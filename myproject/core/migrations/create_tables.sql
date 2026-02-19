-- SQL Server CREATE TABLE statements for Role, Page, and RolePermission tables

-- Create Role table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Role')
BEGIN
    CREATE TABLE [Role] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [RoleName] NVARCHAR(100) NULL,
        [RoleDescription] NVARCHAR(MAX) NULL,
        [IsActive] INT DEFAULT 1,
        [CreatedAt] DATETIME DEFAULT GETDATE(),
        [UpdatedAt] DATETIME DEFAULT GETDATE()
    )
END

-- Create Page table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Page')
BEGIN
    CREATE TABLE [Page] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [PageName] NVARCHAR(100) NULL,
        [PageURL] NVARCHAR(200) NULL,
        [PageIcon] NVARCHAR(50) NULL,
        [IsActive] INT DEFAULT 1,
        [CreatedAt] DATETIME DEFAULT GETDATE()
    )
END

-- Create RolePermission table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RolePermission')
BEGIN
    CREATE TABLE [RolePermission] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [RoleId] INT NOT NULL,
        [PageId] INT NOT NULL,
        [CanView] INT DEFAULT 0,
        [CanAdd] INT DEFAULT 0,
        [CanEdit] INT DEFAULT 0,
        [CanDelete] INT DEFAULT 0,
        [IsActive] INT DEFAULT 1,
        [CreatedAt] DATETIME DEFAULT GETDATE(),
        FOREIGN KEY ([RoleId]) REFERENCES [Role]([Id]),
        FOREIGN KEY ([PageId]) REFERENCES [Page]([Id]),
        CONSTRAINT UQ_RolePage UNIQUE ([RoleId], [PageId])
    )
END

-- Insert some default pages
IF NOT EXISTS (SELECT * FROM [Page])
BEGIN
    INSERT INTO [Page] ([PageName], [PageURL], [PageIcon], [IsActive]) VALUES
    ('Dashboard', '/dashboard/', 'fa-th-large', 1),
    ('Employees', '/employees/', 'fa-users', 1),
    ('Users', '/users/', 'fa-user', 1),
    ('Profile', '/profile/', 'fa-id-card', 1),
    ('Settings', '/settings/', 'fa-cog', 1),
    ('Role', '/settings/role/', 'fa-user-shield', 1),
    ('Role Permission', '/settings/role-permission/', 'fa-shield-alt', 1),
    ('Pages', '/settings/page/', 'fa-file-alt', 1)
END

PRINT 'Tables created successfully!'
