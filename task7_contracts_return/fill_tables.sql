INSERT INTO Client (FullName) VALUES
	(N'������ ���� ��������'),
	(N'������ ϸ�� ��������'),
	(N'������� ������ ���������'),
	(N'�������� ������ ����������'),
	(N'������� ����� ���������'),
	(N'������� ����� ���������')

INSERT INTO [Product] (ProductName) VALUES
	(N'������� 1'),
	(N'������� 2'),
	(N'������� 3'),
	(N'������� 4')


INSERT INTO [ContractType]  (TypeName) VALUES
	(N'��� �������� ����� ����'),
	(N'��� �������� ����� ���'),
	(N'��� �������� ����� ���'),
	(N'��� �������� ����� ������')

INSERT INTO [dbo].[Contract] (ContractTypeID, ProductID, Number, StartDate, EndDate) VALUES
    (1, 1, N'0001', '01-03-2021', '01-05-2021'),
	(1, 1, N'0002', '01-03-2021', '01-05-2021'),
	(2, 1, N'0003', '01-07-2021', '01-09-2021'),
	(1, 1, N'0004', '01-03-2021', '01-06-2021'),
	(2, 1, N'0005', '01-08-2021', '01-10-2021'),
	(1, 1, N'0006', '01-03-2021', '01-06-2021'),
	(2, 1, N'0007', '01-05-2021', '01-09-2021'),
	(1, 1, N'0008', '01-08-2021', '01-10-2021')

INSERT INTO [dbo].[mapContractClient] (ContractID, ClientID) VALUES
    (1, 1),
	(2, 2),
	(3, 2),
	(4, 3),
	(5, 3),
	(6, 4),
	(7, 4),
	(8, 4)

INSERT INTO [dbo].[Service] (ServiceName, StartDate, EndDate) VALUES
	(N'������ 1', '01-03-2021', '01-06-2021'),
	(N'������ 2', '01-05-2021', '01-07-2021'),
	(N'������ 3', '01-04-2021', '01-08-2021'),
	(N'������ 4', '01-06-2021', '01-09-2021')

INSERT INTO [dbo].[Contract] (ContractTypeID, ProductID, Number, StartDate, EndDate) VALUES
    (3, 1, N'0009', NULL, NULL),
	(4, 1, N'0010', NULL, NULL)

INSERT INTO [dbo].[mapContractService] (ContractId, ServiceID) VALUES
	(9, 1),
	(9, 2),
	(9, 3),
	(9, 4),
	(10, 1),
	(10, 4)

INSERT INTO [dbo].[mapContractClient] (ContractID, ClientID) VALUES
    (9, 5),
	(10, 5),
	(10, 6)
