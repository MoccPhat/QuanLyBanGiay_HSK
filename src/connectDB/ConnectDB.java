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
 * Cấu hình kết nối được đọc từ file bên ngoài 'db.properties' để bảo mật thông tin tài khoản (L07).
 */
public class ConnectDB {
    public static Connection con = null;
    private static ConnectDB instance = new ConnectDB();

    public static ConnectDB getInstance() {
        return instance;
    }

    /**
     * Tải thuộc tính kết nối từ file 'db.properties' (tìm tại thư mục gốc ứng dụng hoặc classpath).
     */
    private Properties loadProperties() throws SQLException {
        Properties props = new Properties();
        File propFile = new File("db.properties");
        if (propFile.exists()) {
            try (FileInputStream fis = new FileInputStream(propFile)) {
                props.load(fis);
                return props;
            } catch (Exception e) {
                throw new SQLException("Không thể đọc file cấu hình 'db.properties': " + e.getMessage(), e);
            }
        }

        // Tìm kiếm trên Classpath nếu không thấy ở thư mục làm việc hiện tại
        try (InputStream is = getClass().getClassLoader().getResourceAsStream("db.properties")) {
            if (is != null) {
                props.load(is);
                return props;
            }
        } catch (Exception e) {
            throw new SQLException("Không thể đọc 'db.properties' từ classpath: " + e.getMessage(), e);
        }

        throw new SQLException(
            "Không tìm thấy file cấu hình 'db.properties'!\n" +
            "Vui lòng sao chép 'db.properties.example' thành 'db.properties' tại thư mục gốc và cấu hình URL/User/Password kết nối SQL Server."
        );
    }

    public void connect() throws SQLException {
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch (ClassNotFoundException ignored) {
            // Driver đã được nạp tự động qua ServiceLoader / Classpath
        }

        Properties props = loadProperties();
        String url = props.getProperty("db.url", props.getProperty("url"));
        String user = props.getProperty("db.user", props.getProperty("user"));
        String password = props.getProperty("db.password", props.getProperty("password", ""));

        if (url == null || url.trim().isEmpty()) {
            throw new SQLException("Thiếu thuộc tính 'db.url' trong file 'db.properties'!");
        }
        if (user == null || user.trim().isEmpty()) {
            throw new SQLException("Thiếu thuộc tính 'db.user' trong file 'db.properties'!");
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
