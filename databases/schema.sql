CREATE TABLE `PasteFile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(5000) NOT NULL,
  `filehash` varchar(128) NOT NULL,
  `filemd5` varchar(128) NOT NULL,
  `uploadtime` datetime NOT NULL,
  `mimetype` varchar(256) NOT NULL,
  `size` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `filehash` (`filehash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
