package connectDB;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Quản lý kết nối cơ sở dữ liệu SQL Server theo mẫu thiết kế Singleton trong tầng kết nối dữ liệu.
 */
public class ConnectDB {
    public static Connection con = null;
    private static ConnectDB instance = new ConnectDB();

    /**
     * Lấy thể hiện duy nhất (Singleton instance) của lớp ConnectDB.
     *
     * @return thể hiện duy nhất của ConnectDB
     */
    public static ConnectDB getInstance() {
        return instance;
    }

    /**
     * Mở kết nối đến cơ sở dữ liệu SQL Server QuanLyBanGiay với tài khoản sa.
     *
     * @throws SQLException khi kết nối cơ sở dữ liệu thất bại
     */
    public void connect() throws SQLException {
        String url = "jdbc:sqlserver://localhost:1433;databaseName=QuanLyBanGiay";
        String user = "sa";
        String password = "123456789";
        con = DriverManager.getConnection(url, user, password);
    }

    /**
     * Đóng kết nối cơ sở dữ liệu nếu đang mở.
     */
    public void disconnect() {
        if (con != null)
            try {
                con.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
    }

    /**
     * Lấy đối tượng kết nối Connection hiện tại để thực thi các câu truy vấn SQL.
     *
     * @return đối tượng Connection đang kết nối hoặc null nếu chưa kết nối
     */
    public static Connection getConnection() {
        return con;
    }
}
