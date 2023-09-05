-- Introdução ao Armazenamento e Análise de Dados (IAAD) - BSI/UFRPE
-- Script do Banco de Dados Empresa 

begin;
create schema empresa_adaptado; -- Pode usar o comando 'create database empresa_seunome;' (São semelhantes!)
use empresa_adaptado;

-- Criando as tabelas
create table FUNCIONARIO(
	Pnome VARCHAR(15) NOT NULL,
	Minicial CHAR (1),
	Unome VARCHAR (15) NOT NULL,
	Cpf CHAR(11) NOT NULL,
	Datanasc DATE NOT NULL,
	Endereco VARCHAR(40),
	Sexo CHAR(1),
	Salario decimal(10,2), 
	Cpf_supervisor CHAR(11),
	Dnr INT,
	PRIMARY KEY(Cpf));  -- Aplicando a restrição de chave primária (PK)
create table DEPARTAMENTO(
	Dnome VARCHAR(15) NOT NULL,
	Dnumero INT PRIMARY KEY, -- A chave primária pode ser definida dessa forma ou como na tabela Funcionário.
	Cpf_gerente CHAR(11),
	Data_inicio_gerente DATE,
	UNIQUE(Dnome));
create table DEPENDENTE(
	Fcpf CHAR(11) NOT NULL,
	Nome_dependente VARCHAR(15) NOT NULL,
	Sexo CHAR,
	Datanasc DATE,
	Parentesco VARCHAR(8),
	PRIMARY KEY(Fcpf, Nome_dependente));
	
-- populando/carregando as tabelas do banco de dados
insert into FUNCIONARIO values
	('João','B','Silva','12345678966', '1965-01-09','Rua das flores, 751, São Paulo, SP','M', 30000, '33344555587', 5),
	('Fernando','T','Wong','33344555587', '1955-12-08','Rua da lapa, 34, Sao Paulo, SP','M', 40000, '88866555576', 5),
	('Alice','J','Zelaya','99988777767', '1968-01-19','Rua Souza Lima, 35, Curitiba, PR','F', 25000, '98765432168', 4),
	('Jennifer','S','Souza','98765432168','1941-06-20','Av. Arthur de Lima, 54, Santo Andre, SP','F', 43000, '88866555576', 4),
	('Ronaldo','K','Lima','66688444476','1962-09-15','Rua Rebouças,65, Piracicaba, SP','M', 38000, '33344555587', 5),
	('Joice','A','Leite','45345345376','1972-07-31','Av. Lucas Obes, 74,São Paulo, SP','F', 25000, '33344555587', 5),
	('André','V','Pereira','98798798733','1969-03-29','Rua Timbira, 35,São Paulo, SP','M', 25000, '98765432168', 4),
    ('Jorge','E','Brito','88866555576','1937-11-10','Rua do Horto, 35,São Paulo, SP','M', 55000, NULL, 1);	
 insert into DEPARTAMENTO values
	('Pesquisa',5, '33344555587', '1988-05-22'),
	('Administração',4, '98765432168', '1995-01-01'),
	('Matriz',1, '88866555576', '1981-06-19');		
insert into DEPENDENTE values
	('33344555587', 'Alicia','F', '1986-04-05', 'Filha'),
	('33344555587', 'Tiago','M', '1983-10-25', 'Filho'),
	('33344555587', 'Janaína','F', '1958-05-03', 'Esposa'),
	('98765432168', 'Antonio','M', '1942-02-28', 'Marido'),
	('12345678966', 'Michael','M', '1988-01-04', 'Filho'),
	('12345678966', 'Alice','F', '1988-12-30', 'Filha'),
	('12345678966', 'Elizabeth','F', '1967-05-05', 'Esposa');	

-- Aplicando a restrição de integridade referencial (chaves estrangeiras - FK)
alter table FUNCIONARIO	ADD FOREIGN KEY(Dnr) REFERENCES DEPARTAMENTO(Dnumero) on update cascade on delete cascade;
alter table FUNCIONARIO	ADD FOREIGN KEY(Cpf_supervisor) REFERENCES FUNCIONARIO(Cpf)on update cascade on delete cascade;
alter table DEPARTAMENTO ADD FOREIGN KEY(Cpf_gerente) REFERENCES FUNCIONARIO(Cpf)on update cascade on delete cascade;
alter table DEPENDENTE ADD FOREIGN KEY(Fcpf) REFERENCES FUNCIONARIO(CPF)on update cascade on delete cascade;
commit;
