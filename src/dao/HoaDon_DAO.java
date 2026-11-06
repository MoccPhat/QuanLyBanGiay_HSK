package dao;

import connectDB.ConnectDB;
import entity.*;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;

public class HoaDon_DAO {

    public ArrayList<HoaDon> getAllHoaDon() {
        ArrayList<HoaDon> ds = new ArrayList<>();
        try {
            ConnectDB.getInstance();
            Connection con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }
            String sql = "SELECT h.*, nv.hoTen AS tenNV, kh.hoTen AS tenKH " +
                         "FROM HoaDon h " +
                         "JOIN NhanVien nv ON h.maNhanVien = nv.maNhanVien " +
                         "LEFT JOIN KhachHang kh ON h.maKhachHang = kh.maKhachHang " +
                         "ORDER BY h.ngayLap DESC";
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                String maHD = rs.getString("maHoaDon");
                Timestamp ts = rs.getTimestamp("ngayLap");
                LocalDateTime ngayLap = (ts != null) ? ts.toLocalDateTime() : LocalDateTime.now();
                String maNV = rs.getString("maNhanVien");
                String tenNV = rs.getString("tenNV");
                NhanVien nv = new NhanVien(maNV);
                nv.setHoTen(tenNV);

                String maKH = rs.getString("maKhachHang");
                String tenKH = rs.getString("tenKH");
                KhachHang kh = null;
                if (maKH != null) {
                    kh = new KhachHang(maKH);
                    kh.setHoTen(tenKH);
                }

                double tongTien = rs.getDouble("tongTien");
                String phuongThuc = rs.getString("phuongThucTT");
                double tienKhachDua = rs.getDouble("tienKhachDua");
                double tienThua = rs.getDouble("tienThua");

                HoaDon hd = new HoaDon(maHD, ngayLap, nv, kh, tongTien, phuongThuc, tienKhachDua, tienThua);
                ds.add(hd);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ds;
    }

    public boolean themHoaDon(HoaDon hd) {
        Connection con = null;
        PreparedStatement pstmtHD = null;
        PreparedStatement pstmtCT = null;
        PreparedStatement pstmtKho = null;
        PreparedStatement pstmtDiem = null;

        try {
            ConnectDB.getInstance();
            con = ConnectDB.getConnection();
            if (con == null || con.isClosed()) {
                ConnectDB.getInstance().connect();
                con = ConnectDB.getConnection();
            }

            // Bắt đầu Transaction để bảo toàn toàn vẹn dữ liệu
            con.setAutoCommit(false);

            // 1. Thêm vào bảng HoaDon
            String sqlHD = "INSERT INTO HoaDon (maHoaDon, ngayLap, maNhanVien, maKhachHang, tongTien, phuongThucTT, tienKhachDua, tienThua) " +
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
            pstmtHD = con.prepareStatement(sqlHD);
            pstmtHD.setString(1, hd.getMaHoaDon());
            pstmtHD.setTimestamp(2, Timestamp.valueOf(hd.getNgayLap()));
            pstmtHD.setString(3, hd.getNhanVien().getMaNhanVien());
            if (hd.getKhachHang() != null) {
                pstmtHD.setString(4, hd.getKhachHang().getMaKhachHang());
            } else {
                pstmtHD.setNull(4, Types.VARCHAR);
            }
            pstmtHD.setDouble(5, hd.getTongTien());
            pstmtHD.setString(6, hd.getPhuongThucTT());
            pstmtHD.setDouble(7, hd.getTienKhachDua());
            pstmtHD.setDouble(8, hd.getTienThua());
            pstmtHD.executeUpdate();

            // 2. Thêm từng dòng vào ChiTietHoaDon và trừ tồn kho
            String sqlCT = "INSERT INTO ChiTietHoaDon (maHoaDon, maChiTietGiay, soLuong, donGia, giamGia, thanhTien) " +
                           "VALUES (?, ?, ?, ?, ?, ?)";
            pstmtCT = con.prepareStatement(sqlCT);

            String sqlKho = "UPDATE ChiTietGiay SET soLuongTon = soLuongTon - ? WHERE maChiTietGiay = ? AND soLuongTon >= ?";
            pstmtKho = con.prepareStatement(sqlKho);

            for (ChiTietHoaDon ct : hd.getDanhSachChiTiet()) {
                // Thêm chi tiết hóa đơn
                pstmtCT.setString(1, hd.getMaHoaDon());
                pstmtCT.setString(2, ct.getChiTietGiay().getMaChiTietGiay());
                pstmtCT.setInt(3, ct.getSoLuong());
                pstmtCT.setDouble(4, ct.getDonGia());
                pstmtCT.setDouble(5, ct.getGiamGia());
                pstmtCT.setDouble(6, ct.getThanhTien());
                pstmtCT.executeUpdate();

                // Trừ số lượng tồn kho của size tương ứng
                pstmtKho.setInt(1, ct.getSoLuong());
                pstmtKho.setString(2, ct.getChiTietGiay().getMaChiTietGiay());
                pstmtKho.setInt(3, ct.getSoLuong());
                int rowsUpdated = pstmtKho.executeUpdate();
                if (rowsUpdated == 0) {
                    // Không đủ tồn kho -> Rollback lập tức
                    con.rollback();
                    System.err.println("Lỗi: Không đủ số lượng tồn kho cho mã " + ct.getChiTietGiay().getMaChiTietGiay());
                    return false;
                }
            }

            // 3. Tích điểm cho khách hàng (Mỗi 100.000 VNĐ được cộng 1 điểm)
            if (hd.getKhachHang() != null && hd.getTongTien() > 0) {
                int diemCong = (int) (hd.getTongTien() / 100000.0);
                String sqlDiem = "UPDATE KhachHang SET diemTichLuy = diemTichLuy + ? WHERE maKhachHang = ?";
                pstmtDiem = con.prepareStatement(sqlDiem);
                pstmtDiem.setInt(1, diemCong);
                pstmtDiem.setString(2, hd.getKhachHang().getMaKhachHang());
                pstmtDiem.executeUpdate();
            }

            // Cam kết giao dịch (Commit)
            con.commit();
            return true;

        } catch (SQLException e) {
            e.printStackTrace();
            if (con != null) {
                try {
                    con.rollback(); // Rollback nếu có bất kỳ lỗi nào
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
            return false;
        } finally {
            if (con != null) {
                try {
                    con.setAutoCommit(true);
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
