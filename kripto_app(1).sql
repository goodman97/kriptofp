-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 07, 2025 at 04:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kripto_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender` varchar(100) NOT NULL,
  `receiver` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `msg_type` varchar(20) NOT NULL DEFAULT 'text',
  `filename` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender`, `receiver`, `message`, `timestamp`, `msg_type`, `filename`) VALUES
(1, 'fu', 'user_b', 'gPCMFPcCx6SPwkqJwh47DQ==', '2025-11-04 12:19:31', 'text', NULL),
(2, 'kentut', 'user_b', '0FkIebWHghhELuFEvgqQNA==', '2025-11-04 12:20:16', 'text', NULL),
(3, 'fu', 'user_b', '2cjrBOKwNnhlNzYOJ+JMRA==', '2025-11-04 12:57:40', 'text', NULL),
(4, 'fu', 'user_b', 'YOHynMFdXkvTEXZULWR9ww==', '2025-11-05 00:09:47', 'text', NULL),
(5, 'fu', 'martis', 'inez', '2025-11-05 02:32:42', 'text', NULL),
(6, 'kentut', 'fu', 'h', '2025-11-05 08:48:17', 'text', NULL),
(7, 'fu', 'kentut', 'yrih', '2025-11-05 08:49:00', 'text', NULL),
(8, 'kentut', 'fu', 'fkJ[id vmrwpctzlw :m.dur]twm', '2025-11-05 10:59:18', 'file', 'spam.csv.enc'),
(9, 'fu', 'kentut', 'fkJ[id vmrwpctzlQ :mplxqAGZ uj.M]j', '2025-11-05 11:17:23', 'file', 'Modul VIII.pdf.enc'),
(15, 'fu', 'kentut', 'gcK[ besiilqqseumxyvxj :_mkob_wjsxxihr.l]x', '2025-11-05 13:37:58', 'stegano', 'stego_fu_kentut.png'),
(16, 'kentut', 'fu', 'nwfe', '2025-11-06 10:54:15', 'text', NULL),
(17, 'fu', 'kentut', 'h', '2025-11-06 10:54:35', 'text', NULL),
(18, 'kentut', 'fu', 'rth', '2025-11-06 10:55:23', 'text', NULL),
(19, 'fu', 'kentut', 'bwvt', '2025-11-06 10:55:37', 'text', NULL),
(20, 'fu', 'kentut', 'inez', '2025-11-06 10:55:46', 'text', NULL),
(21, 'kentut', 'fu', 'kez', '2025-11-06 10:55:55', 'text', NULL),
(22, 'fu', 'kentut', 'bwvt', '2025-11-06 13:51:44', 'text', NULL),
(23, 'fu', 'kentut', 'ciehsbf ', '2025-11-06 13:51:55', 'text', NULL),
(24, 'kentut', 'fu', 'cieh', '2025-11-06 13:52:00', 'text', NULL),
(25, 'fu', 'kentut', 'hcoaysl mee d euxsks', '2025-11-06 13:52:09', 'text', NULL),
(26, 'kentut', 'fu', 'ctezvkl um gkcectsp nc', '2025-11-06 13:53:02', 'text', NULL),
(27, 'fu', 'kentut', 'ulrsp', '2025-11-06 13:53:13', 'text', NULL),
(28, 'kentut', 'fu', 'eqasoyarmagybi', '2025-11-06 13:53:21', 'text', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(256) NOT NULL,
  `last_active` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `last_active`) VALUES
(1, 'martis', '9fbb9e42930bd3c25b8238030e97136de5e305a756b975ebebafc158a51a417e', '2025-11-05 00:59:18'),
(2, 'fu', '6d50451024109d96ae2743a1a90dedec1677e6ff29b7063f9a3c2da4b52796a9', '2025-11-06 13:51:22'),
(3, 'kentut', '14ea62f0fddb95fafb6352cfa2885f2a1257fb272e49361c700782b7b822d446', '2025-11-06 13:51:26');

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `update_last_active` BEFORE UPDATE ON `users` FOR EACH ROW BEGIN
  SET NEW.last_active = CURRENT_TIMESTAMP;
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
