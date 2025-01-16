import sqlite3

# Create/connect to the SQLite database
conn = sqlite3.connect('ReActAgent/NetworkAutomationAgent/FakeNetwork/networkdb/devices.db')
cursor = conn.cursor()

# Create the device_metadata table
cursor.execute('''
CREATE TABLE IF NOT EXISTS device_metadata (
    asset_number INTEGER PRIMARY KEY,
    device_name TEXT,
    device_platform TEXT,
    device_ip TEXT,
    username TEXT,
    password TEXT
)
''')

# Insert a record into the device_metadata table
cursor.execute('''
INSERT INTO device_metadata (asset_number, device_name, device_platform, device_ip, username, password)
VALUES (?, ?, ?, ?, ?, ?)
''', (1, 'cisco_ce_sea3.agg', 'cisco_ios', '127.0.0.1', 'admin', 'admin'))

cursor.execute('''
INSERT INTO device_metadata (asset_number, device_name, device_platform, device_ip, username, password)
VALUES (?, ?, ?, ?, ?, ?)
''', (2, 'arista_core_sea3.agg', 'arista_eos', '127.0.0.1', 'admin', 'admin'))


cursor.execute('''
INSERT INTO device_metadata (asset_number, device_name, device_platform, device_ip, username, password)
VALUES (?, ?, ?, ?, ?, ?)
''', (3, 'jun_border_sea3.bor', 'juniper_junos', '127.0.0.1', 'admin', 'admin'))


# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created, and entry added successfully.")
