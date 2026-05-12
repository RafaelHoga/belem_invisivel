-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema belem_invisivel
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belem_invisivel
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belem_invisivel` DEFAULT CHARACTER SET utf8 ;
USE `belem_invisivel` ;

-- -----------------------------------------------------
-- Table `belem_invisivel`.`PERFIL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`PERFIL` (
  `ID_perfil` INT NOT NULL AUTO_INCREMENT,
  `descricao_perfil` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID_perfil`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`USUARIO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`USUARIO` (
  `ID_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome_usuario` VARCHAR(75) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(30) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `PERFIL_ID_perfil` INT NOT NULL,
  PRIMARY KEY (`ID_usuario`, `PERFIL_ID_perfil`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `senha_UNIQUE` (`senha` ASC) VISIBLE,
  INDEX `fk_USUARIO_PERFIL_idx` (`PERFIL_ID_perfil` ASC) VISIBLE,
  CONSTRAINT `fk_USUARIO_PERFIL`
    FOREIGN KEY (`PERFIL_ID_perfil`)
    REFERENCES `belem_invisivel`.`PERFIL` (`ID_perfil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`CATEGORIAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`CATEGORIAS` (
  `ID_categoria` INT NOT NULL AUTO_INCREMENT,
  `descricao_categoria` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`PONTO_TURISTICO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`PONTO_TURISTICO` (
  `ID_ponto_turistico` INT NOT NULL AUTO_INCREMENT,
  `nome_ponto_turistico` VARCHAR(45) NOT NULL,
  `telefone` VARCHAR(20) NULL,
  `descricao` TEXT NOT NULL,
  `rua` VARCHAR(150) NULL,
  `cidade` VARCHAR(100) NOT NULL,
  `CATEGORIAS_ID_categoria` INT NOT NULL,
  PRIMARY KEY (`ID_ponto_turistico`, `CATEGORIAS_ID_categoria`),
  INDEX `fk_PONTO_TURISTICO_CATEGORIAS1_idx` (`CATEGORIAS_ID_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_PONTO_TURISTICO_CATEGORIAS1`
    FOREIGN KEY (`CATEGORIAS_ID_categoria`)
    REFERENCES `belem_invisivel`.`CATEGORIAS` (`ID_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`SUGESTAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`SUGESTAO` (
  `id_sugestao` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(255) NOT NULL,
  `endereco` VARCHAR(300) NOT NULL,
  `nome_sugestao` VARCHAR(290) NOT NULL,
  `USUARIO_ID_usuario` INT NOT NULL,
  `CATEGORIAS_ID_categoria` INT NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id_sugestao`),
  INDEX `fk_SUGESTAO_USUARIO1_idx` (`USUARIO_ID_usuario` ASC) VISIBLE,
  INDEX `fk_SUGESTAO_CATEGORIAS1_idx` (`CATEGORIAS_ID_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_SUGESTAO_USUARIO1`
    FOREIGN KEY (`USUARIO_ID_usuario`)
    REFERENCES `belem_invisivel`.`USUARIO` (`ID_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SUGESTAO_CATEGORIAS1`
    FOREIGN KEY (`CATEGORIAS_ID_categoria`)
    REFERENCES `belem_invisivel`.`CATEGORIAS` (`ID_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`FAVORITO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`FAVORITO` (
  `USUARIO_ID_usuario` INT NOT NULL,
  `PONTO_TURISTICO_ID_ponto_turistico` INT NOT NULL,
  `data_favorito` DATE NOT NULL,
  PRIMARY KEY (`USUARIO_ID_usuario`, `PONTO_TURISTICO_ID_ponto_turistico`),
  INDEX `fk_USUARIO_has_PONTO_TURISTICO_PONTO_TURISTICO1_idx` (`PONTO_TURISTICO_ID_ponto_turistico` ASC) VISIBLE,
  INDEX `fk_USUARIO_has_PONTO_TURISTICO_USUARIO1_idx` (`USUARIO_ID_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_USUARIO_has_PONTO_TURISTICO_USUARIO1`
    FOREIGN KEY (`USUARIO_ID_usuario`)
    REFERENCES `belem_invisivel`.`USUARIO` (`ID_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_USUARIO_has_PONTO_TURISTICO_PONTO_TURISTICO1`
    FOREIGN KEY (`PONTO_TURISTICO_ID_ponto_turistico`)
    REFERENCES `belem_invisivel`.`PONTO_TURISTICO` (`ID_ponto_turistico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belem_invisivel`.`AVALIACAO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belem_invisivel`.`AVALIACAO` (
  `PONTO_TURISTICO_ID_ponto_turistico` INT NOT NULL,
  `USUARIO_ID_usuario` INT NOT NULL,
  `mensagem` VARCHAR(300) NOT NULL,
  `estrela` INT NOT NULL,
  `id_avaliacao` INT NOT NULL,
  PRIMARY KEY (`PONTO_TURISTICO_ID_ponto_turistico`, `USUARIO_ID_usuario`, `id_avaliacao`),
  INDEX `fk_PONTO_TURISTICO_has_USUARIO_USUARIO1_idx` (`USUARIO_ID_usuario` ASC) VISIBLE,
  INDEX `fk_PONTO_TURISTICO_has_USUARIO_PONTO_TURISTICO1_idx` (`PONTO_TURISTICO_ID_ponto_turistico` ASC) VISIBLE,
  CONSTRAINT `fk_PONTO_TURISTICO_has_USUARIO_PONTO_TURISTICO1`
    FOREIGN KEY (`PONTO_TURISTICO_ID_ponto_turistico`)
    REFERENCES `belem_invisivel`.`PONTO_TURISTICO` (`ID_ponto_turistico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PONTO_TURISTICO_has_USUARIO_USUARIO1`
    FOREIGN KEY (`USUARIO_ID_usuario`)
    REFERENCES `belem_invisivel`.`USUARIO` (`ID_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

SELECT * FROM categorias;

-- INSERINDO DADOS NA TABELA categorias

INSERT INTO categorias (descricao_categoria) VALUES
('Ponto turistico'),
('Restaurante'),
('Hospitais'),
('Hoteis');


-- INSERINDO DADOS NA TABELA ponto_turistico

SELECT * FROM ponto_turistico;

INSERT INTO ponto_turistico (nome_ponto_turistico,telefone,descricao,rua,cidade,CATEGORIAS_ID_categoria) VALUES
('Estação das Docas','9198965790','A Estação das Docas é um complexo turístico, gastronômico e cultural de referência, localizado na orla da Baía do Guajará',' Av Boulevard Castilho s/n','Belém',1),
('Ilha de cotijuba',Null,'A Ilha de Cotijuba é  conhecida por ser um refúgio de água doce com cerca de 20 km de praias paradisíacas e ritmo tranquilo','S-Rua','Belém',1),
('Hotel Ibis Style Hangar','919993456','O ibis Styles Belém Hangar é um hotel perto do aeroporto de Belém, ideal para quem quer aproveitar o melhor da capital do Pará.','Avenida duque de caxias 1538 Marco','Belém','2'),
('Hospitais Porto Dias','91987657890','O Hospital Porto Dias, é um centro médico de alta complexidade e referência na região Norte, inaugurado em 1995. Destaca-se por sua infraestrutura moderna, oferecendo atendimento 24h, urgência/emergência, UTI.','Av. Almirante Barroso, n 1454, Marco – Belém – PA','Belém',3),
('Familia Sicilia','9198765432','O restaurante Famiglia Sicilia ver a comida como a alma do corpo','Avenida Concelheiro Furtado 1420 Batista Campos','Belém',2);

SELECT * FROM ponto_turistico;
SELECT * FROM perfil;

INSERT INTO perfil(descricao_perfil) VALUES
('administrador'),
('comum'); 

-- INSERINDO DADOS NA TABELA usuario

SELECT * FROM usuario;

INSERT INTO usuario(nome_usuario,email,senha,data_nascimento,PERFIL_ID_perfil) VALUES
('Gabriel Henrique Duarte Portal','gabriell6790@gmail.com','123456','2005-01-09',1),
('Rafael japones','rafael123@gmail.com',23456,'1998-02-08',1),
('João Santista','joao5678@gmail.com','34567','2000-01-04',1),
('Renan Nascimento','renan6789@gmail.com','45678','2001-02-06',2),
('Rodrigo Pinto','rodrigo1234@gmail.com','12345','2002-01-12',2);

SELECT * FROM favorito;
-- INSERINDO DADOS NA TABELA favorito

INSERT INTO favorito (USUARIO_ID_usuario,PONTO_TURISTICO_ID_ponto_turistico,data_favorito) VALUES 
(11,1,'2026-01-31'),
(12,1,'2025-02-28'),
(13,2,'2024-03-31'); 

SELECT * FROM avaliacao;

ALTER TABLE avaliacao
DROP COLUMN id_avaliacao;
INSERT INTO avaliacao (PONTO_TURISTICO_ID_ponto_turistico,USUARIO_ID_usuario,mensagem,estrela) VALUES
(2,11,'muito bom, recomendo',5);



