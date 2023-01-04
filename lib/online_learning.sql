/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : online_learning

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 04/01/2023 11:59:55
*/
DROP DATABASE IF EXISTS `online_learning`;
CREATE DATABASE IF NOT EXISTS `online_learning`;
USE `online_learning`;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for original_event
-- ----------------------------
DROP TABLE IF EXISTS `original_event`;
CREATE TABLE `original_event`  (
  `counter` int(0) NOT NULL AUTO_INCREMENT,
  `student_id` int(0) NOT NULL,
  `event_key` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `event_value` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `record_time` datetime(0) NULL,
  PRIMARY KEY (`counter`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 221 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of original_event
-- ----------------------------
INSERT INTO `original_event` VALUES (1, 1, '1', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (2, 1, '2', '1', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (3, 1, '3', '1', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (4, 1, '4', '1', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (5, 1, '5', '1', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (6, 1, '6', '1', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (7, 1, '7', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (8, 1, '8', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (9, 1, '9', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (10, 1, '10', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (11, 1, '11', '0', '2022-12-28 12:31:54');
INSERT INTO `original_event` VALUES (12, 1, '1', '3', '2022-12-28 12:31:55');
INSERT INTO `original_event` VALUES (13, 1, '3', '0', '2022-12-28 12:31:55');
INSERT INTO `original_event` VALUES (14, 1, '4', '0', '2022-12-28 12:31:55');
INSERT INTO `original_event` VALUES (15, 1, '6', '0', '2022-12-28 12:31:55');
INSERT INTO `original_event` VALUES (16, 1, '8', '1', '2022-12-28 12:31:55');
INSERT INTO `original_event` VALUES (17, 1, '2', '0', '2022-12-28 12:31:57');
INSERT INTO `original_event` VALUES (18, 1, '8', '0', '2022-12-28 12:31:57');
INSERT INTO `original_event` VALUES (19, 1, '9', '1', '2022-12-28 12:31:57');
INSERT INTO `original_event` VALUES (20, 1, '2', '1', '2022-12-28 12:31:58');
INSERT INTO `original_event` VALUES (21, 1, '1', '0', '2022-12-28 12:31:59');
INSERT INTO `original_event` VALUES (22, 1, '3', '1', '2022-12-28 12:31:59');
INSERT INTO `original_event` VALUES (23, 1, '4', '1', '2022-12-28 12:31:59');
INSERT INTO `original_event` VALUES (24, 1, '6', '1', '2022-12-28 12:31:59');
INSERT INTO `original_event` VALUES (25, 1, '9', '0', '2022-12-28 12:31:59');
INSERT INTO `original_event` VALUES (26, 1, '1', '3', '2022-12-28 12:32:02');
INSERT INTO `original_event` VALUES (27, 1, '2', '0', '2022-12-28 12:32:02');
INSERT INTO `original_event` VALUES (28, 1, '3', '0', '2022-12-28 12:32:02');
INSERT INTO `original_event` VALUES (29, 1, '4', '0', '2022-12-28 12:32:02');
INSERT INTO `original_event` VALUES (30, 1, '6', '0', '2022-12-28 12:32:02');
INSERT INTO `original_event` VALUES (31, 1, '1', '4', '2022-12-28 12:32:05');
INSERT INTO `original_event` VALUES (32, 1, '2', '1', '2022-12-28 12:32:05');
INSERT INTO `original_event` VALUES (33, 1, '3', '1', '2022-12-28 12:32:05');
INSERT INTO `original_event` VALUES (34, 1, '4', '1', '2022-12-28 12:32:05');
INSERT INTO `original_event` VALUES (35, 1, '1', '3', '2022-12-28 12:32:06');
INSERT INTO `original_event` VALUES (36, 1, '2', '0', '2022-12-28 12:32:06');
INSERT INTO `original_event` VALUES (37, 1, '3', '0', '2022-12-28 12:32:06');
INSERT INTO `original_event` VALUES (38, 1, '4', '0', '2022-12-28 12:32:06');
INSERT INTO `original_event` VALUES (39, 1, '6', '1', '2022-12-28 12:32:08');
INSERT INTO `original_event` VALUES (40, 1, '6', '0', '2022-12-28 12:32:09');
INSERT INTO `original_event` VALUES (41, 1, '1', '1', '2022-12-28 12:32:12');
INSERT INTO `original_event` VALUES (42, 1, '1', '4', '2022-12-28 12:32:13');
INSERT INTO `original_event` VALUES (43, 1, '1', '3', '2022-12-28 12:32:15');
INSERT INTO `original_event` VALUES (44, 1, '9', '1', '2022-12-28 12:32:15');
INSERT INTO `original_event` VALUES (45, 1, '10', '1', '2022-12-28 12:32:15');
INSERT INTO `original_event` VALUES (46, 1, '9', '0', '2022-12-28 12:32:16');
INSERT INTO `original_event` VALUES (47, 1, '10', '0', '2022-12-28 12:32:16');
INSERT INTO `original_event` VALUES (48, 1, '9', '1', '2022-12-28 12:32:17');
INSERT INTO `original_event` VALUES (49, 1, '3', '1', '2022-12-28 12:32:18');
INSERT INTO `original_event` VALUES (50, 1, '1', '0', '2022-12-28 12:32:20');
INSERT INTO `original_event` VALUES (51, 1, '4', '1', '2022-12-28 12:32:20');
INSERT INTO `original_event` VALUES (52, 1, '9', '0', '2022-12-28 12:32:20');
INSERT INTO `original_event` VALUES (53, 1, '3', '0', '2022-12-28 12:32:21');
INSERT INTO `original_event` VALUES (54, 1, '4', '0', '2022-12-28 12:32:21');
INSERT INTO `original_event` VALUES (55, 1, '1', '3', '2022-12-28 12:32:22');
INSERT INTO `original_event` VALUES (56, 1, '6', '1', '2022-12-28 12:32:22');
INSERT INTO `original_event` VALUES (57, 1, '6', '0', '2022-12-28 12:32:24');
INSERT INTO `original_event` VALUES (58, 1, '9', '1', '2022-12-28 12:32:25');
INSERT INTO `original_event` VALUES (59, 1, '9', '0', '2022-12-28 12:32:26');
INSERT INTO `original_event` VALUES (60, 1, '1', '0', '2022-12-28 12:58:42');
INSERT INTO `original_event` VALUES (61, 1, '2', '1', '2022-12-28 12:58:42');
INSERT INTO `original_event` VALUES (62, 1, '3', '1', '2022-12-28 12:58:42');
INSERT INTO `original_event` VALUES (63, 1, '4', '1', '2022-12-28 12:58:42');
INSERT INTO `original_event` VALUES (64, 1, '5', '0', '2022-12-28 12:58:42');
INSERT INTO `original_event` VALUES (65, 1, '6', '1', '2022-12-28 12:58:43');
INSERT INTO `original_event` VALUES (66, 1, '2', '0', '2022-12-28 12:58:44');
INSERT INTO `original_event` VALUES (67, 1, '5', '1', '2022-12-28 12:58:44');
INSERT INTO `original_event` VALUES (68, 1, '6', '0', '2022-12-28 12:58:44');
INSERT INTO `original_event` VALUES (69, 1, '2', '1', '2022-12-28 12:58:45');
INSERT INTO `original_event` VALUES (70, 1, '1', '3', '2022-12-28 12:58:48');
INSERT INTO `original_event` VALUES (71, 1, '3', '0', '2022-12-28 12:58:48');
INSERT INTO `original_event` VALUES (72, 1, '4', '0', '2022-12-28 12:58:48');
INSERT INTO `original_event` VALUES (73, 1, '8', '1', '2022-12-28 12:58:48');
INSERT INTO `original_event` VALUES (74, 1, '1', '0', '2022-12-28 12:58:49');
INSERT INTO `original_event` VALUES (75, 1, '3', '1', '2022-12-28 12:58:49');
INSERT INTO `original_event` VALUES (76, 1, '4', '1', '2022-12-28 12:58:49');
INSERT INTO `original_event` VALUES (77, 1, '6', '1', '2022-12-28 12:58:49');
INSERT INTO `original_event` VALUES (78, 1, '8', '0', '2022-12-28 12:58:49');
INSERT INTO `original_event` VALUES (79, 1, '6', '0', '2022-12-28 12:58:51');
INSERT INTO `original_event` VALUES (80, 1, '1', '3', '2022-12-28 12:58:52');
INSERT INTO `original_event` VALUES (81, 1, '6', '1', '2022-12-28 12:58:52');
INSERT INTO `original_event` VALUES (82, 1, '2', '0', '2022-12-28 12:58:54');
INSERT INTO `original_event` VALUES (83, 1, '3', '0', '2022-12-28 12:58:54');
INSERT INTO `original_event` VALUES (84, 1, '4', '0', '2022-12-28 12:58:54');
INSERT INTO `original_event` VALUES (85, 1, '6', '0', '2022-12-28 12:58:54');
INSERT INTO `original_event` VALUES (86, 1, '2', '1', '2022-12-28 12:58:55');
INSERT INTO `original_event` VALUES (87, 1, '3', '1', '2022-12-28 12:58:55');
INSERT INTO `original_event` VALUES (88, 1, '4', '1', '2022-12-28 12:58:55');
INSERT INTO `original_event` VALUES (89, 1, '6', '1', '2022-12-28 12:58:55');
INSERT INTO `original_event` VALUES (90, 1, '1', '0', '2022-12-28 12:58:56');
INSERT INTO `original_event` VALUES (91, 1, '9', '1', '2022-12-28 12:58:56');
INSERT INTO `original_event` VALUES (92, 1, '9', '0', '2022-12-28 12:58:57');
INSERT INTO `original_event` VALUES (93, 1, '1', '3', '2022-12-28 12:59:00');

-- ----------------------------
-- Table structure for original_event_key
-- ----------------------------
DROP TABLE IF EXISTS `original_event_key`;
CREATE TABLE `original_event_key`  (
  `event_type` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `event_key` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of original_event_key
-- ----------------------------
INSERT INTO `original_event_key` VALUES ('emotion', '1');
INSERT INTO `original_event_key` VALUES ('is_pitch', '2');
INSERT INTO `original_event_key` VALUES ('is_yaw', '3');
INSERT INTO `original_event_key` VALUES ('is_roll', '4');
INSERT INTO `original_event_key` VALUES ('is_z_gap', '5');
INSERT INTO `original_event_key` VALUES ('is_y_gap_sh', '6');
INSERT INTO `original_event_key` VALUES ('is_y_head_gap', '7');
INSERT INTO `original_event_key` VALUES ('is_per', '8');
INSERT INTO `original_event_key` VALUES ('is_blink', '9');
INSERT INTO `original_event_key` VALUES ('is_yawn', '10');
INSERT INTO `original_event_key` VALUES ('is_close', '11');

-- ----------------------------
-- Table structure for original_event_value
-- ----------------------------
DROP TABLE IF EXISTS `original_event_value`;
CREATE TABLE `original_event_value`  (
  `event_key` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_value` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of original_event_value
-- ----------------------------
INSERT INTO `original_event_value` VALUES ('1', '1');
INSERT INTO `original_event_value` VALUES ('1', '2');
INSERT INTO `original_event_value` VALUES ('1', '3');
INSERT INTO `original_event_value` VALUES ('1', '4');
INSERT INTO `original_event_value` VALUES ('1', '5');
INSERT INTO `original_event_value` VALUES ('1', '6');
INSERT INTO `original_event_value` VALUES ('1', '7');
INSERT INTO `original_event_value` VALUES ('1', '8');
INSERT INTO `original_event_value` VALUES ('2', '0');
INSERT INTO `original_event_value` VALUES ('2', '1');
INSERT INTO `original_event_value` VALUES ('3', '0');
INSERT INTO `original_event_value` VALUES ('3', '1');
INSERT INTO `original_event_value` VALUES ('4', '0');
INSERT INTO `original_event_value` VALUES ('4', '1');
INSERT INTO `original_event_value` VALUES ('5', '0');
INSERT INTO `original_event_value` VALUES ('5', '1');
INSERT INTO `original_event_value` VALUES ('6', '0');
INSERT INTO `original_event_value` VALUES ('6', '1');
INSERT INTO `original_event_value` VALUES ('7', '0');
INSERT INTO `original_event_value` VALUES ('7', '1');
INSERT INTO `original_event_value` VALUES ('8', '0');
INSERT INTO `original_event_value` VALUES ('8', '1');
INSERT INTO `original_event_value` VALUES ('9', '0');
INSERT INTO `original_event_value` VALUES ('9', '1');
INSERT INTO `original_event_value` VALUES ('10', '0');
INSERT INTO `original_event_value` VALUES ('10', '1');
INSERT INTO `original_event_value` VALUES ('11', '0');
INSERT INTO `original_event_value` VALUES ('11', '1');

-- ----------------------------
-- Table structure for parent_info
-- ----------------------------
DROP TABLE IF EXISTS `parent_info`;
CREATE TABLE `parent_info`  (
  `parent_id` int(0) NOT NULL,
  `parent_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_sex` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_tel` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_pswd` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `student_id` int(0) NOT NULL,
  PRIMARY KEY (`parent_id`) USING BTREE,
  INDEX `student_id_idx`(`student_id`) USING BTREE,
  CONSTRAINT `student_id` FOREIGN KEY (`student_id`) REFERENCES `student_info` (`student_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of parent_info
-- ----------------------------
INSERT INTO `parent_info` VALUES (1, 'Nancy', 'woman', '123456', '123456@gmail.com', '123456', 1);

-- ----------------------------
-- Table structure for student_info
-- ----------------------------
DROP TABLE IF EXISTS `student_info`;
CREATE TABLE `student_info`  (
  `student_id` int(0) NOT NULL,
  `student_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `student_sex` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `student_pswd` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`student_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_info
-- ----------------------------
INSERT INTO `student_info` VALUES (1, 'Fancy', 'woman', '123456');

-- ----------------------------
-- Table structure for study_state
-- ----------------------------
DROP TABLE IF EXISTS `study_state`;
CREATE TABLE `study_state`  (
  `counter` int(0) NOT NULL AUTO_INCREMENT,
  `student_id` int(0) NOT NULL,
  `state_key` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `state_value` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `record_time` datetime(0) NULL,
  PRIMARY KEY (`counter`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of study_state
-- ----------------------------
INSERT INTO `study_state` VALUES (1, 1, '1', '2', '2022-12-28 12:32:23');
INSERT INTO `study_state` VALUES (2, 1, '2', '1', '2022-12-28 12:32:23');
INSERT INTO `study_state` VALUES (3, 1, '3', '4', '2022-12-28 12:32:23');
INSERT INTO `study_state` VALUES (4, 1, '4', '3', '2022-12-28 12:32:23');

-- ----------------------------
-- Table structure for study_state_key
-- ----------------------------
DROP TABLE IF EXISTS `study_state_key`;
CREATE TABLE `study_state_key`  (
  `state_type` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `state_key` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of study_state_key
-- ----------------------------
INSERT INTO `study_state_key` VALUES ('emotion', '1');
INSERT INTO `study_state_key` VALUES ('fatigue', '2');
INSERT INTO `study_state_key` VALUES ('posture', '3');
INSERT INTO `study_state_key` VALUES ('focus', '4');

-- ----------------------------
-- Table structure for study_state_value
-- ----------------------------
DROP TABLE IF EXISTS `study_state_value`;
CREATE TABLE `study_state_value`  (
  `state_key` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `state_value` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of study_state_value
-- ----------------------------
INSERT INTO `study_state_value` VALUES ('1', '1');
INSERT INTO `study_state_value` VALUES ('1', '2');
INSERT INTO `study_state_value` VALUES ('1', '3');
INSERT INTO `study_state_value` VALUES ('2', '1');
INSERT INTO `study_state_value` VALUES ('2', '2');
INSERT INTO `study_state_value` VALUES ('2', '3');
INSERT INTO `study_state_value` VALUES ('2', '4');
INSERT INTO `study_state_value` VALUES ('2', '5');
INSERT INTO `study_state_value` VALUES ('3', '1');
INSERT INTO `study_state_value` VALUES ('3', '2');
INSERT INTO `study_state_value` VALUES ('3', '3');
INSERT INTO `study_state_value` VALUES ('3', '4');
INSERT INTO `study_state_value` VALUES ('4', '1');
INSERT INTO `study_state_value` VALUES ('4', '2');
INSERT INTO `study_state_value` VALUES ('4', '3');
INSERT INTO `study_state_value` VALUES ('4', '4');

SET FOREIGN_KEY_CHECKS = 1;
