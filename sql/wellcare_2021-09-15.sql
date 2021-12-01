# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.29)
# Database: wellcare
# Generation Time: 2020-12-23 14:59:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

# Dump of table wellcare_reservation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
	`id` BIGINT(19) NOT NULL AUTO_INCREMENT,
	`user_name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '이름' COLLATE 'utf8mb4_0900_ai_ci',
	`user_birth` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '생년월일' COLLATE 'utf8mb4_0900_ai_ci',
	`user_gender` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '성별' COLLATE 'utf8mb4_0900_ai_ci',
	`user_phone` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '휴대폰번호' COLLATE 'utf8mb4_0900_ai_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '등록일',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;

DROP TABLE IF EXISTS `resv_consultation`;

CREATE TABLE `resv_consultation` (
	`id` INT(6) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
	`resv_date` DATE NOT NULL COMMENT '예약날짜',
	`resv_time` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '예약시간' COLLATE 'utf8mb4_bin',
	`user_id` BIGINT(19) NOT NULL DEFAULT '0' COMMENT 'User ID',
	`clinical_trial_type` BIGINT(19) NOT NULL DEFAULT '0' COMMENT '문진타입',
	`resv_flag` INT(10) NOT NULL DEFAULT '0' COMMENT '예약상태 (0: 예약완료 / 1: 예약취소 / 2: 관리자 추가 / 3: 관리자 취소 / 4: 관리자 예약 변경',
	`resv_cancel_note` VARCHAR(255) NULL DEFAULT NULL COMMENT '예약취소사유' COLLATE 'utf8mb4_bin',
	`clinical_trial_flag` TINYINT(3) NOT NULL DEFAULT '0' COMMENT '문진상태',
	`diagnosis_flag` TINYINT(3) NOT NULL DEFAULT '0' COMMENT '검사상태',
	`create_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK_resv_consaltation_user` (`user_id`) USING BTREE,
	INDEX `FK_resv_consultation_clinical_trial` (`clinical_trial_type`) USING BTREE,
	CONSTRAINT `FK_resv_consultation_clinical_trial` FOREIGN KEY (`clinical_trial_type`) REFERENCES `reservation`.`clinical_trial` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `FK_resv_consultation_user` FOREIGN KEY (`user_id`) REFERENCES `reservation`.`user` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB
;

DROP TABLE IF EXISTS `resv_consultaion_limit`;

CREATE TABLE `resv_consultation_limit` (
	`id` BIGINT(19) NOT NULL AUTO_INCREMENT,
	`hour` INT(10) NOT NULL,
	`minute` INT(10) NOT NULL,
	`limit` INT(10) NOT NULL,
	`create_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB
;

DROP TABLE IF EXISTS `admin_account`;

CREATE TABLE `admin_account` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`admin_id` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '아이디' COLLATE 'utf8mb4_0900_ai_ci',
	`password` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '비밀번호' COLLATE 'utf8mb4_0900_ai_ci',
	`name` VARCHAR(255) NULL DEFAULT NULL COMMENT '이름' COLLATE 'utf8mb4_0900_ai_ci',
	`email` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '이메일' COLLATE 'utf8mb4_0900_ai_ci',
	`phone` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '가입일',
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `email` (`email`) USING BTREE,
	UNIQUE INDEX `user_id` (`admin_id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=7
;

DROP TABLE IF EXISTS `admin_account_token`;

CREATE TABLE `admin_account_token` (
	`aid` INT(10) NOT NULL AUTO_INCREMENT,
	`admin_id` VARCHAR(255) NULL DEFAULT NULL COMMENT 'admin 로그인 ID' COLLATE 'utf8mb4_0900_ai_ci',
	`token` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_login` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`aid`) USING BTREE,
	INDEX `FK1_admin_account_token_admin_account` (`admin_id`) USING BTREE,
	CONSTRAINT `FK1_admin_account_token_admin_account` FOREIGN KEY (`admin_id`) REFERENCES `reservation`.`admin_account` (`admin_id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=8
;

DROP TABLE IF EXISTS `notice`;

CREATE TABLE `notice` (
	`id` BIGINT(19) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`content` LONGTEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`important` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`is_file` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`author` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `notice_file`;

CREATE TABLE `notice_file` (
	`id` BIGINT(19) NOT NULL AUTO_INCREMENT,
	`notice_id` BIGINT(19) NOT NULL,
	`file_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`file_path` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;
