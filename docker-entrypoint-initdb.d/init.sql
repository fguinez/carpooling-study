SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for trips
-- ----------------------------
DROP TABLE IF EXISTS `trips`;
CREATE TABLE `trips` (
  `id` int auto_increment,
  `region` varchar(255) DEFAULT NULL,
  `origin_x` float DEFAULT NULL,
  `origin_y` float DEFAULT NULL,
  `destination_x` float DEFAULT NULL,
  `destination_y` float DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  `datasource` varchar(255) DEFAULT NULL,
  primary key(id)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;