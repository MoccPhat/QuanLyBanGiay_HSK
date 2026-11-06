package connectDB;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectDB {
    public static Connection con = null;
    private static ConnectDB instance = new ConnectDB();

    public static ConnectDB getInstance() {
        return instance;
    }

    public void connect() throws SQLException {
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch (ClassNotFoundException e) {
            // Driver loaded via classpath
        }

        // Danh sách các cổng và cấu hình kết nối tự động (ưu tiên TCP 1433 và timeout nhanh)
        String[] urls = {
            "jdbc:sqlserver://localhost:1433;databaseName=QuanLyBanGiay;encrypt=false;trustServerCertificate=true;loginTimeout=3;",
            "jdbc:sqlserver://127.0.0.1:1433;databaseName=QuanLyBanGiay;encrypt=false;trustServerCertificate=true;loginTimeout=3;",
            "jdbc:sqlserver://localhost\\SQLEXPRESS;databaseName=QuanLyBanGiay;encrypt=false;trustServerCertificate=true;loginTimeout=3;"
        };
        String[] passwords = {"123456789", "sapassword", "123456"};

        SQLException lastEx = null;
        for (String url : urls) {
            for (String pass : passwords) {
                try {
                    con = DriverManager.getConnection(url, "sa", pass);
                    if (con != null && !con.isClosed()) {
                        System.out.println(">>> Kết nối Microsoft SQL Server thành công! (URL: " + url + ", User: sa)");
                        return;
                    }
                } catch (SQLException ex) {
                    lastEx = ex;
                }
            }
        }

        if (con == null && lastEx != null) {
            throw lastEx;
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
