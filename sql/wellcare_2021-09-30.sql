# ************************************************************
-- # Sequel Pro SQL dump
-- # Version 4541
#
-- # http://www.sequelpro.com/
-- # https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 8.0.23)
# Database: reservation
-- # Generation Time: 2020-12-23 14:59:07 +0000
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
CREATE DATABASE 'reservation';
USE 'reservation';

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`user_name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '이름' COLLATE 'utf8mb4_general_ci',
	`user_birth` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '생년월일' COLLATE 'utf8mb4_general_ci',
	`user_gender` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '성별' COLLATE 'utf8mb4_general_ci',
	`user_phone` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '휴대폰번호' COLLATE 'utf8mb4_general_ci',
	`user_memo` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '메모' COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '등록일',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `resv_consultation`;

CREATE TABLE `resv_consultation` (
	`id` INT(10) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
	`resv_date` DATE NULL DEFAULT NULL COMMENT '예약날짜',
	`resv_time` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '예약시간' COLLATE 'utf8mb4_general_ci',
	`user_id` BIGINT(20) NOT NULL DEFAULT '0' COMMENT 'User ID',
	`clinical_trial_type` BIGINT(20) NOT NULL DEFAULT '0' COMMENT '문진타입',
	`resv_flag` INT(10) NOT NULL DEFAULT '0' COMMENT '예약상태 (0: 예약완료 / 1: 예약취소 / 2: 관리자 추가 / 3: 관리자 취소 / 4: 관리자 예약 변경',
	`resv_cancel_note` VARCHAR(255) NULL DEFAULT NULL COMMENT '예약취소사유' COLLATE 'utf8mb4_general_ci',
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
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `resv_consultaion_limit`;

CREATE TABLE `resv_consultation_limit` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`hour` VARCHAR(255) NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`limit` INT(10) NOT NULL,
	`create_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `admin_account`;

CREATE TABLE `admin_account` (
	`id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
	`admin_id` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '아이디' COLLATE 'utf8mb4_general_ci',
	`password` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '비밀번호' COLLATE 'utf8mb4_general_ci',
	`name` VARCHAR(255) NULL DEFAULT NULL COMMENT '이름' COLLATE 'utf8mb4_general_ci',
	`email` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '이메일' COLLATE 'utf8mb4_general_ci',
	`phone` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '가입일',
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `email` (`email`) USING BTREE,
	UNIQUE INDEX `user_id` (`admin_id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `admin_account_token`;

CREATE TABLE `admin_account_token` (
	`aid` BIGINT(20) UNSIGNED NOT NULL,
	`token` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`last_login` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

DROP TABLE IF EXISTS `clinical_trial`;

CREATE TABLE `clinical_trial` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '문진타입id',
	`title` VARCHAR(255) NULL DEFAULT '0' COMMENT '문진제목' COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


DROP TABLE IF EXISTS `notice`;

CREATE TABLE `notice` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`content` LONGTEXT NOT NULL COLLATE 'utf8mb4_general_ci',
	`important` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci',
	`is_file` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci',
	`author` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `notice_file`;

CREATE TABLE `notice_file` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`notice_id` BIGINT(20) NOT NULL,
	`file_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`file_path` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `holiday`;

CREATE TABLE `holiday` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`date` VARCHAR(255) NOT NULL DEFAULT '0' COMMENT '날짜' COLLATE 'utf8mb4_general_ci',
	`text` VARCHAR(255) NOT NULL DEFAULT '0' COMMENT '공휴일 설명' COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY (`id`) USING BTREE
)
COMMENT='공휴일'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;





# ************************************************************
-- # Sequel Pro SQL dump
-- # Version 4541
#
-- # http://www.sequelpro.com/
-- # https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 8.0.23)
# Database: clinical_db
-- # Generation Time: 2020-12-23 14:59:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

# Dump of table wellcare_clinical_db
# ************************************************************
CREATE DATABASE `questionnaire`;
USE `questionnaire`;

DROP TABLE IF EXISTS `agree`;

CREATE TABLE `agree` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_name` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_birth` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_gender` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_phone` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY (`id`) USING BTREE
)
COMMENT='동의서'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `agree_photos`;

CREATE TABLE `agree_photos` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL,
	`agree_image1` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image2` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image3` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image4` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image5` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image6` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image7` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image8` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`agree_image9` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_AGREE_PHOTOS` (`agree_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_AGREE_PHOTOS` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COMMENT='동의서 사진'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


DROP TABLE IF EXISTS `complete_check`;

CREATE TABLE `complete_check` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`common_flag` INT(10) NOT NULL DEFAULT '0',
	`nutrition_flag` INT(10) NOT NULL DEFAULT '0',
	`cognitive_flag` INT(10) NOT NULL DEFAULT '0',
	`mental_flag` INT(10) NOT NULL DEFAULT '0',
	`stress_flag` INT(10) NOT NULL DEFAULT '0',
	`stomach_flag` INT(10) NOT NULL DEFAULT '0',
	`sleep_flag` INT(10) NOT NULL DEFAULT '0',
	`samkim_flag` INT(10) NOT NULL DEFAULT '0',
	`fatigue_flag` INT(10) NOT NULL DEFAULT '0',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_COMPLETE_CHECK` (`agree_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_COMPLETE_CHECK` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='문진표 작성 여부'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `common_question`;

CREATE TABLE `common_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`category_id` BIGINT(20) NOT NULL DEFAULT '0' COMMENT '1: 질환력 / 2: 흡연 / 3: 음주 / 4: 신체활동',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`answer` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '1',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_COMMON` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_COMMON` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_COMMON` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_COMMON` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='건강검진 종합 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `nutrition_question`;

CREATE TABLE `nutrition_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_NUTRITION` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_NUTRITION` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_NUTRITION` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_NUTRITION` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='영양 생활습관 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `cognitive_question`;

CREATE TABLE `cognitive_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_COGNITIVE` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_COGNITIVE` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_COGNITIVE` FOREIGN KEY (`agree_id`) REFERENCES `clinical_db`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_COGNITIVE` FOREIGN KEY (`question_type_id`) REFERENCES `clinical_db`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='인지기능  설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `mental_question`;

CREATE TABLE `mental_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_MENTAL` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_MENTAL` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_MENTAL` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_MENTAL` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='정신건강 검사'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `stress_question`;

CREATE TABLE `stress_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_STRESS` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_STRESS` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_STRESS` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_STRESS` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='스트레스 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `stomach_question`;

CREATE TABLE `stomach_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_STOMACH` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_STOMACH` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_STOMACH` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_STOMACH` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='위장건강 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `sleep_question`;

CREATE TABLE `sleep_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_SLEEP` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_SLEEP` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_SLEEP` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_SLEEP` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='수면장애 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `fatigue_question`;

CREATE TABLE `fatigue_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(209) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_FATIGUE` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_FATIGUE` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_FATIGUE` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_FATIGUE` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`question_category` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='피로도 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `samkim_question`;

CREATE TABLE `samkim_question` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL DEFAULT '0',
	`answer` VARCHAR(255) NOT NULL DEFAULT '' COLLATE 'utf8mb4_general_ci',
	`answer_text` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	`modified_date` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	`question_type_id` BIGINT(20) NOT NULL DEFAULT '2',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK1_AGREE_SAMKIM` (`agree_id`) USING BTREE,
	INDEX `FK2_QUESTION_CATEGORY_SAMKIM` (`question_type_id`) USING BTREE,
	CONSTRAINT `FK1_AGREE_SAMKIM` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK2_QUESTION_CATEGORY_SAMKIM` FOREIGN KEY (`question_type_id`) REFERENCES `questionnaire`.`samkim_question` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='삼킴 설문'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `question_category`;

CREATE TABLE `question_category` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`type` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`create_date` DATETIME NOT NULL DEFAULT current_timestamp(),
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

DROP TABLE IF EXISTS `checkup_list`;

CREATE TABLE `checkup_list` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`agree_id` BIGINT(20) NOT NULL,
	`wash_flag` INT(10) NOT NULL DEFAULT '0',
	`agree_flag` INT(10) NOT NULL DEFAULT '0',
	`blood_flag` INT(10) NOT NULL DEFAULT '0',
	`hair_flag` INT(10) NOT NULL DEFAULT '0',
	`skinmv_flag` INT(10) NOT NULL DEFAULT '0',
	`bowel_flag` INT(10) NOT NULL DEFAULT '0',
	`hrv_flag` INT(10) NOT NULL DEFAULT '0',
	`body_flag` INT(10) NOT NULL DEFAULT '0',
	`mind_flag` INT(10) NOT NULL DEFAULT '0',
	`brain_flag` INT(10) NOT NULL DEFAULT '0',
	`skin_flag` INT(10) NOT NULL DEFAULT '0',
	`eye_flag` INT(10) NOT NULL DEFAULT '0',
	`exercise_flag` INT(10) NOT NULL DEFAULT '0',
	`smart_flag` INT(10) NOT NULL DEFAULT '0',
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`modified_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `CHECKUP_LIST_AGREE_ID` (`agree_id`) USING BTREE,
	CONSTRAINT `CHECKUP_LIST_AGREE_ID` FOREIGN KEY (`agree_id`) REFERENCES `questionnaire`.`agree` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

