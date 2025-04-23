-- Insert into Member (Shop Owners) with relative file paths
INSERT INTO member (name, image, age, email, contact_number) VALUES
('Rahul Sharma', '"images/m1.jpg"', 35, 'rahul.sharma@email.com', '9876543210'),
('Aisha Verma', '"images/f1.jpg"', 30, 'aisha.verma@email.com', '8765432109'),
('Vikram Patel', '"images/m2.jpg"', 40, 'vikram.patel@email.com', '7654321098'),
('Neha Agarwal', '"images/f2.jpg"', 32, 'neha.agarwal@email.com', '6543210987'),
('Ravi Mehta', '"images/m3.jpg"', 38, 'ravi.mehta@email.com', '9432109876'),
('Sneha Roy', '"images/f3.jpg"', 29, 'sneha.roy@email.com', '8321098765'),
('Arjun Singh', '"images/m4.jpg"', 36, 'arjun.singh@email.com', '7210987654'),
('Priya Das', '"images/f4.jpg"', 28, 'priya.das@email.com', '6109876543'),
('Manoj Nair', '"images/m5.jpg"', 42, 'manoj.nair@email.com', '9098765432'),
('Kavita Joshi', '"images/f5.jpg"', 34, 'kavita.joshi@email.com', '8987654321'),
('Rohit Malhotra', '"images/m6.jpg"', 31, 'rohit.malhotra@email.com', '7876543210'),
('Anjali Reddy', '"images/f6.jpg"', 27, 'anjali.reddy@email.com', '6765432109');

-- Insert into Shop
INSERT INTO shop (shop_id, name, address, contact, member_id) VALUES
('AB101', 'Fresh Mart', 'Shop No. 1, Maninagar, Ahmedabad, Gujarat 380008', '9988776655', 1),
('CD202', 'Daily Needs', '12, Satellite Road, Ahmedabad, Gujarat 380015', '8877665544', 2),
('EF303', 'Grocery World', '45, Vastrapur, Ahmedabad, Gujarat 380015', '7766554433', 3),
('GH404', 'Super Bazaar', '3, Navrangpura, Ahmedabad, Gujarat 380009', '6655443322', 4),
('IJ505', 'Family Store', 'Shop 7, Paldi, Ahmedabad, Gujarat 380007', '9544332211', 5),
('KL606', 'Mega Mart', '101, Bodakdev, Ahmedabad, Gujarat 380054', '8433221100', 6),
('MN707', 'Quick Buy', '22, Ellisbridge, Ahmedabad, Gujarat 380006', '7322110099', 7),
('OP808', 'Happy Mart', '15, SG Highway, Ahmedabad, Gujarat 380060', '6211009988', 8),
('QR909', 'Discount Store', '8, Naranpura, Ahmedabad, Gujarat 380013', '9100998877', 9),
('ST111', 'Easy Shop', '33, Thaltej, Ahmedabad, Gujarat 380059', '8099887766', 10),
('UV222', 'Local Market', '17, Memnagar, Ahmedabad, Gujarat 380052', '7199776655', 11),
('WX333', 'Budget Mart', '9, Chandkheda, Ahmedabad, Gujarat 382424', '6299665544', 12);

-- Insert into Customer
INSERT INTO customer (customer_id, name, contact, email) VALUES
('RS9876543210', 'Ramesh Sharma', '9876543210', 'ramesh.sharma@email.com'),
('AV8765432109', 'Ananya Verma', '8765432109', 'ananya.verma@email.com'),
('VP7654321098', 'Vikas Patel', '7654321098', 'vikas.patel@email.com'),
('NA6543210987', 'Neha Arora', '6543210987', 'neha.arora@email.com'),
('RM9432109876', 'Rohan Mehta', '9432109876', 'rohan.mehta@email.com'),
('SR8321098765', 'Sonal Roy', '8321098765', 'sonal.roy@email.com'),
('AS7210987654', 'Amit Singh', '7210987654', 'amit.singh@email.com'),
('PD6109876543', 'Priyanka Das', '6109876543', 'priyanka.das@email.com'),
('MN9098765432', 'Mohan Nair', '9098765432', 'mohan.nair@email.com'),
('KJ8987654321', 'Kiran Joshi', '8987654321', 'kiran.joshi@email.com'),
('RM7876543210', 'Raj Malhotra', '7876543210', 'raj.malhotra@email.com'),
('AR6765432109', 'Aarti Reddy', '6765432109', 'aarti.reddy@email.com');

-- Insert into Supplier
INSERT INTO supplier (supplier_id, name, contact, email, address) VALUES
('SYRA12345', 'Rajesh Suppliers', '9123456789', 'rajesh.suppliers@email.com', 'GIDC, Vatva, Ahmedabad, Gujarat 382445'),
('SYAN23456', 'Anil Distributors', '9234567890', 'anil.distributors@email.com', 'Naroda Industrial Area, Ahmedabad, Gujarat 382330'),
('SYVI34567', 'Vikas Enterprises', '9345678901', 'vikas.enterprises@email.com', 'Odhav, Ahmedabad, Gujarat 382415'),
('SYMO45678', 'Mohan Traders', '9456789012', 'mohan.traders@email.com', 'Bapunagar, Ahmedabad, Gujarat 380024'),
('SYKA56789', 'Karan Suppliers', '9567890123', 'karan.suppliers@email.com', 'Sabarmati, Ahmedabad, Gujarat 380005'),
('SYAM67890', 'Amit Wholesalers', '9678901234', 'amit.wholesalers@email.com', 'Kalupur, Ahmedabad, Gujarat 380001'),
('SYPR78901', 'Priya Distributors', '9789012345', 'priya.distributors@email.com', 'Manek Chowk, Ahmedabad, Gujarat 380001'),
('SYSU89012', 'Suresh Traders', '9890123456', 'suresh.traders@email.com', 'Rakhial, Ahmedabad, Gujarat 380023'),
('SYNE90123', 'Neha Enterprises', '9901234567', 'neha.enterprises@email.com', 'Gota, Ahmedabad, Gujarat 382481'),
('SYRO01234', 'Rohan Suppliers', '9012345678', 'rohan.suppliers@email.com', 'Isanpur, Ahmedabad, Gujarat 382443');

-- Insert into Product
INSERT INTO product (name, category, supplier_id, shop_id, price, stock_quantity) VALUES
('Rice', 'Grocery', 'SYRA12345', 'AB101', 50.00, 100),
('Wheat Flour', 'Grocery', 'SYAN23456', 'CD202', 40.00, 80),
('Sugar', 'Grocery', 'SYVI34567', 'EF303', 45.00, 50),
('Milk', 'Dairy', 'SYMO45678', 'GH404', 30.00, 60),
('Oil', 'Grocery', 'SYKA56789', 'IJ505', 120.00, 40),
('Bread', 'Bakery', 'SYAM67890', 'KL606', 25.00, 90),
('Salt', 'Grocery', 'SYPR78901', 'MN707', 15.00, 200),
('Butter', 'Dairy', 'SYSU89012', 'OP808', 50.00, 30),
('Tea', 'Beverages', 'SYNE90123', 'QR909', 80.00, 70),
('Soap', 'Personal Care', 'SYRO01234', 'ST111', 20.00, 150);

-- Insert into Order
INSERT INTO `order` (customer_id, shop_id, order_date, total_amount, status) VALUES
('RS9876543210', 'AB101', NOW(), 500.00, 'Completed'),
('AV8765432109', 'CD202', NOW(), 1000.00, 'Pending'),
('VP7654321098', 'EF303', NOW(), 300.00, 'Completed'),
('NA6543210987', 'GH404', NOW(), 750.00, 'Pending'),
('RM9432109876', 'IJ505', NOW(), 600.00, 'Cancelled'),
('SR8321098765', 'KL606', NOW(), 450.00, 'Completed'),
('AS7210987654', 'MN707', NOW(), 200.00, 'Pending'),
('PD6109876543', 'OP808', NOW(), 800.00, 'Completed'),
('MN9098765432', 'QR909', NOW(), 350.00, 'Pending'),
('KJ8987654321', 'ST111', NOW(), 150.00, 'Completed');

-- Insert into Order Details
INSERT INTO order_details (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 100.00),
(2, 2, 5, 200.00),
(3, 3, 3, 135.00),
(4, 4, 10, 300.00),
(5, 5, 2, 240.00),
(6, 6, 5, 125.00),
(7, 7, 10, 150.00),
(8, 8, 4, 200.00),
(9, 9, 2, 160.00),
(10, 10, 5, 100.00);

-- Insert into Employee
INSERT INTO employee (name, role, contact, shop_id, salary, salary_status) VALUES
('Suresh Kumar', 'Cashier', '7896541230', 'AB101', 15000.00, 'Pending'),
('Meena Gupta', 'Manager', '8896541231', 'CD202', 25000.00, 'Paid'),
('Rakesh Yadav', 'Sales', '9896541232', 'EF303', 12000.00, 'Pending'),
('Pooja Sharma', 'Cashier', '6796541233', 'GH404', 14000.00, 'Paid'),
('Vijay Patel', 'Stock Keeper', '7796541234', 'IJ505', 13000.00, 'Pending'),
('Anita Roy', 'Manager', '8796541235', 'KL606', 27000.00, 'Paid'),
('Kunal Singh', 'Sales', '9796541236', 'MN707', 11000.00, 'Pending'),
('Deepa Nair', 'Cashier', '6896541237', 'OP808', 15000.00, 'Paid'),
('Ajay Joshi', 'Stock Keeper', '7896541238', 'QR909', 12500.00, 'Pending'),
('Rina Das', 'Sales', '8896541239', 'ST111', 11500.00, 'Paid');

-- Insert into Payment
INSERT INTO payment (order_id, amount, method) VALUES
(1, 500.00, 'Cash'),
(2, 1000.00, 'UPI'),
(3, 300.00, 'Debit'),
(4, 750.00, 'Credit'),
(5, 600.00, 'Cash'),
(6, 450.00, 'UPI'),
(7, 200.00, 'Loyalty points'),
(8, 800.00, 'Debit'),
(9, 350.00, 'Credit'),
(10, 150.00, 'Cash');

-- Insert into Attendance
INSERT INTO attendance (employee_id, attendance_date, check_in, check_out, status) VALUES
(1, '2025-02-25', '09:00:00', '18:00:00', 'Present'),
(2, '2025-02-25', '10:00:00', '19:00:00', 'Present'),
(3, '2025-02-25', '09:30:00', '17:30:00', 'Present'),
(4, '2025-02-25', '08:00:00', NULL, 'Absent'),
(5, '2025-02-25', '09:00:00', '18:00:00', 'Present'),
(6, '2025-02-25', '10:00:00', '19:00:00', 'Present'),
(7, '2025-02-25', '09:00:00', '17:00:00', 'Present'),
(8, '2025-02-25', '08:30:00', '16:30:00', 'Present'),
(9, '2025-02-25', '09:00:00', NULL, 'On Leave'),
(10, '2025-02-25', '09:00:00', '18:00:00', 'Present');

-- Insert into Loyalty
INSERT INTO loyalty (customer_id, shop_id, purchase_amount, loyalty_points, purchase_date) VALUES
('RS9876543210', 'AB101', 500.00, 50, '2025-02-20'),
('AV8765432109', 'CD202', 1000.00, 100, '2025-02-21'),
('VP7654321098', 'EF303', 300.00, 30, '2025-02-22'),
('NA6543210987', 'GH404', 750.00, 75, '2025-02-23'),
('RM9432109876', 'IJ505', 600.00, 60, '2025-02-24'),
('SR8321098765', 'KL606', 450.00, 45, '2025-02-25'),
('AS7210987654', 'MN707', 200.00, 20, '2025-02-26'),
('PD6109876543', 'OP808', 800.00, 80, '2025-02-27'),
('MN9098765432', 'QR909', 350.00, 35, '2025-02-28'),
('KJ8987654321', 'ST111', 150.00, 15, '2025-03-01');

SHOW TABLES;
