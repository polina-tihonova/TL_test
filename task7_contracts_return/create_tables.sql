USE [polinadb_contracts]
GO

CREATE TABLE [dbo].[Contract](
	ContractID INT IDENTITY(1,1) NOT NULL,  
	ContractTypeID INT NOT NULL, 
	ProductID INT NULL, 
	Number NVARCHAR(20) NOT NULL, 
	StartDate DATE NULL, 
	EndDate DATE NULL
)
GO

CREATE TABLE [dbo].[ContractType](
	ContractTypeID INT IDENTITY(1,1) NOT NULL,  
	TypeName NVARCHAR(30) NOT NULL

)
GO

CREATE TABLE [dbo].[Product](
	ProductID INT IDENTITY(1,1) NOT NULL, 
	ProductName NVARCHAR(30) NOT NULL
)
GO

CREATE TABLE [dbo].[Client](
	ClientID INT IDENTITY(1,1) NOT NULL, 
	FullName NVARCHAR(30) NOT NULL
)
GO

CREATE TABLE [dbo].[Service](
	ServiceID INT IDENTITY(1,1) NOT NULL, 
	ServiceName NVARCHAR(30) NOT NULL, 
	StartDate DATE NOT NULL, 
	EndDate DATE NOT NULL
)
GO

CREATE TABLE [dbo].[mapContractClient](
	ContractID INT NOT NULL, 
	ClientID INT NOT NULL
)
GO

CREATE TABLE [dbo].[mapContractService](
	ContractID INT NOT NULL, 
	ServiceID INT NOT NULL
)
GO

CREATE TABLE [dbo].[mapServiceProduct](
	ServiceID INT NOT NULL,
	ProductID INT NOT NULL
)
GO

