-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 07, 2025 at 09:22 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

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
(16, 'kentut', 'fu', 'fkJ[id vmrwpctzlQ :mvvnc 6 scV - omsjklU_big.awlhxgj]', '2025-11-05 14:24:49', 'file', 'Materi 6 - Block Chipper_new.pptx.enc'),
(17, 'kentut', 'fu', 'gcK[ besiilqqseumxyvxj :_mkokhgod_dyhr.m]x', '2025-11-05 14:25:35', 'stegano', 'stego_kentut_fu.png'),
(18, 'fu', 'kentut', 'rth', '2025-11-05 14:26:37', 'text', NULL),
(19, 'fu', 'kentut', ' uiLced', '2025-11-06 04:27:49', 'text', NULL),
(20, 'kentut', 'fu', 'unik dedcpskkq gmk woh', '2025-11-06 12:15:10', 'text', NULL),
(21, 'fu', 'kentut', 'vsl', '2025-11-06 12:15:38', 'text', NULL),
(22, 'kentut', 'fu', ' uilpkiigqar', '2025-11-06 12:40:27', 'text', NULL),
(23, 'kentut', 'fu', 'ofeoy', '2025-11-06 12:40:43', 'text', NULL),
(24, 'kentut', 'fu', ' gsOyw', '2025-11-06 12:47:06', 'text', NULL),
(25, 'kentut', 'fu', 'cueeil y qmjkwzv', '2025-11-06 12:47:23', 'text', NULL),
(26, 'fu', 'kentut', 'eq', '2025-11-06 12:47:40', 'text', NULL),
(27, 'fu', 'kentut', ' ueexxibls', '2025-11-06 12:51:17', 'text', NULL),
(28, 'kentut', 'fu', '.', '2025-11-06 12:51:29', 'text', NULL),
(29, 'kentut', 'fu', 'oqz', '2025-11-06 12:51:35', 'text', NULL),
(30, 'fu', 'kentut', 'h', '2025-11-06 12:51:39', 'text', NULL),
(31, 'kentut', 'fu', ' kraecigcf lll', '2025-11-06 12:52:20', 'text', NULL),
(32, 'kentut', 'fu', 'h', '2025-11-06 12:52:22', 'text', NULL),
(33, 'kentut', 'fu', 'h', '2025-11-06 12:52:25', 'text', NULL),
(34, 'kentut', 'fu', 'gcpsk orgo ypii lkcv', '2025-11-06 12:52:36', 'text', NULL),
(35, 'fu', 'kentut', 'h', '2025-11-06 12:58:09', 'text', NULL),
(36, 'kentut', 'fu', 'yrihizig', '2025-11-06 12:58:44', 'text', NULL),
(37, 'fu', 'kentut', 'h', '2025-11-06 12:58:54', 'text', NULL),
(38, 'fu', 'kentut', 'gumtevpzf', '2025-11-06 13:03:56', 'text', NULL),
(39, 'fu', 'kentut', ' uilpkiigqarxmb k', '2025-11-06 13:04:07', 'text', NULL),
(40, 'kentut', 'fu', 'yrihig', '2025-11-06 13:28:50', 'text', NULL),
(41, 'kentut', 'fu', 'gcK[ besiilqqseumxyvxj :_mkokhgod_dyhr.m]x', '2025-11-06 13:29:25', 'stegano', 'stego_kentut_fu.png'),
(42, 'Faisal', 'fu', 'uiL', '2025-11-07 07:49:42', 'text', NULL),
(43, 'Faisal', 'fu', 'ineZjsw s', '2025-11-07 07:49:48', 'text', NULL),
(44, 'fu', 'Faisal', 'uiL', '2025-11-07 07:50:05', 'text', NULL),
(45, 'Faisal', 'fu', 'fkJ[id vmrwpctzlQ :mvvnc 6 scV - omsjklU_big.awlhxgj]', '2025-11-07 07:50:25', 'file', 'Materi 6 - Block Chipper_new.pptx.enc'),
(46, 'Faisal', 'fu', 'gcK[ besiilqqseumxyvxj :_mkojccJd_vehr.m]x', '2025-11-07 08:16:36', 'stegano', 'stego_Faisal_fu.png'),
(47, 'Faisal', 'fu', 'fkJ[id vmrwpctzl1 :m32322900iuO_YrsxoPmblkvxHM_yD_U-wseysu.1]bm', '2025-11-07 08:20:14', 'file', '123230092_MartinAjiNugraha_IF-D_Tugas1.docx.enc');

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
(2, 'fu', '6d50451024109d96ae2743a1a90dedec1677e6ff29b7063f9a3c2da4b52796a9', '2025-11-07 07:49:24'),
(12, 'Faisal', '03380b058dc76315323d4e5bc5d8c5855ebcd0fec627c646d467014420eedf6a', '2025-11-07 07:48:47');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
