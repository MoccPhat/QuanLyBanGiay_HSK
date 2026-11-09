package connectDB;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/**
 * Lớp quản lý kết nối cơ sở dữ liệu Microsoft SQL Server (Singleton pattern).
 * Cấu hình kết nối ưu tiên đọc từ file bên ngoài 'db.properties' để bảo mật thông tin tài khoản (L07).
 * Tên CSDL thực tế của đồ án: QuanLyBanGiay (khác với tên bài mẫu QLNVIEN của môn học).
 * Chuỗi kết nối tuân thủ định dạng chuẩn của Microsoft SQL Server JDBC Driver.
 */
public class ConnectDB {
    // Chuỗi URL mẫu chuẩn mực trỏ vào database thật QuanLyBanGiay
    // Ghi chú quan trọng: Tên CSDL thực tế của đồ án là QuanLyBanGiay (khác với QLNVIEN trong giáo trình/bài mẫu)
    public static final String DEFAULT_URL = 
        "jdbc:sqlserver://localhost:1433;databasename=QuanLyBanGiay;encrypt=false;trustServerCertificate=true;loginTimeout=3;";
    public static final String DEFAULT_USER = "sa";

    public static Connection con = null;
    private static ConnectDB instance = new ConnectDB();

    public static ConnectDB getInstance() {
        return instance;
    }

    /**
     * Tải thuộc tính kết nối từ file 'db.properties' (tìm tại thư mục gốc ứng dụng hoặc classpath).
     */
    private Properties loadProperties() {
        Properties props = new Properties();
        File propFile = new File("db.properties");
        if (propFile.exists()) {
            try (FileInputStream fis = new FileInputStream(propFile)) {
                props.load(fis);
                return props;
            } catch (Exception e) {
                System.err.println("Cảnh báo: Không thể đọc file cấu hình 'db.properties': " + e.getMessage());
            }
        }

        // Tìm kiếm trên Classpath nếu không thấy ở thư mục làm việc hiện tại
        try (InputStream is = getClass().getClassLoader().getResourceAsStream("db.properties")) {
            if (is != null) {
                props.load(is);
                return props;
            }
        } catch (Exception e) {
            System.err.println("Cảnh báo: Không thể đọc 'db.properties' từ classpath: " + e.getMessage());
        }

        return props;
    }

    public void connect() throws SQLException {
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch (ClassNotFoundException ignored) {
            // Driver đã được nạp tự động qua ServiceLoader / Classpath
        }

        Properties props = loadProperties();

        // Chuỗi kết nối mẫu chuẩn mực theo yêu cầu đồ án:
        // String url = "jdbc:sqlserver://localhost:1433;databasename=QuanLyBanGiay;";
        // Ưu tiên đọc từ 'db.properties', nếu không có cấu hình thì dùng DEFAULT_URL trỏ vào CSDL thật QuanLyBanGiay
        String url = props.getProperty("db.url", props.getProperty("url"));
        if (url == null || url.trim().isEmpty()) {
            // Ghi chú: Tên CSDL thực tế của đồ án là QuanLyBanGiay (khác với bài mẫu QLNVIEN của môn học)
            url = DEFAULT_URL;
        }

        // Đọc user & password từ db.properties, KHÔNG hard-code mật khẩu
        String user = props.getProperty("db.user", props.getProperty("user", DEFAULT_USER));
        String password = props.getProperty("db.password", props.getProperty("password", ""));

        if (user == null || user.trim().isEmpty()) {
            user = DEFAULT_USER;
        }
        if (password == null) {
            password = "";
        }

        // Đảm bảo loginTimeout=3 nếu chưa có trong URL để tránh treo giao diện lâu
        if (!url.toLowerCase().contains("logintimeout")) {
            url = url.endsWith(";") ? url + "loginTimeout=3;" : url + ";loginTimeout=3;";
        }

        con = DriverManager.getConnection(url, user, password);
        if (con != null && !con.isClosed()) {
            System.out.println(">>> Kết nối Microsoft SQL Server thành công! (URL: " + url + ", User: " + user + ")");
        }
    }

    public void disconnect() {
        if (con != null) {
            try {
                con.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public static Connection getConnection() {
        try {
            if (con == null || con.isClosed()) {
                instance.connect();
            }
        } catch (SQLException e) {
            System.err.println("Lỗi tự động kết nối CSDL: " + e.getMessage());
        }
        return con;
    }
}
