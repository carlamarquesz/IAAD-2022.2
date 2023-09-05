CREATE TABLE FUNCIONARIO_LOG (
    Cpf VARCHAR(11),
    DataModificacao TIMESTAMP,
    DetalhesModificacao TEXT
);

DELIMITER //

CREATE TRIGGER Funcionario_AfterUpdate
AFTER UPDATE ON funcionario
FOR EACH ROW
BEGIN
    INSERT INTO FUNCIONARIO_LOG (Cpf, DataModificacao, DetalhesModificacao)
    VALUES (NEW.Cpf, NOW(), CONCAT('Registro atualizado: ', OLD.Pnome, ' ', OLD.Unome));
END;
//

DELIMITER ;
