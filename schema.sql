-- SQLite schema for storing budget request submissions
CREATE TABLE IF NOT EXISTS submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  message TEXT NOT NULL,
  budget_amount TEXT,
  budget_package TEXT,
  selected_features TEXT,
  payment_status TEXT,
  client_sent_at TEXT,
  submitted_at TEXT NOT NULL
);

-- If you prefer a MySQL schema, use this version instead:
--
-- CREATE TABLE submissions (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   name VARCHAR(255) NOT NULL,
--   email VARCHAR(255) NOT NULL,
--   phone VARCHAR(50),
--   message TEXT NOT NULL,
--   budget_amount VARCHAR(50),
--   budget_package VARCHAR(255),
--   selected_features TEXT,
--   payment_status VARCHAR(50),
--   client_sent_at DATETIME,
--   submitted_at DATETIME NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
