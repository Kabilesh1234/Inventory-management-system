-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 09, 2025 at 09:30 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `customer_relationship_emp`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `rt_cart`
--

CREATE TABLE `rt_cart` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `price` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `check_st` int(11) NOT NULL,
  `av_product` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `deliver_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_cart`
--

INSERT INTO `rt_cart` (`id`, `uname`, `pid`, `status`, `rdate`, `price`, `category`, `quantity`, `amount`, `bill_id`, `check_st`, `av_product`, `retailer`, `deliver_st`) VALUES
(1, 'gokul', 2, 1, '11-11-2022', 1000, 'Shoes', 2, 2000, 2, 0, 0, '', 0),
(2, 'gokul', 1, 1, '11-11-2022', 455, 'Men-Shirt', 2, 910, 2, 0, 0, '', 1),
(3, 'vijay', 2, 0, '11-11-2022', 1000, 'Shoes', 4, 4000, 0, 1, 3, '', 0),
(4, 'vijay', 4, 1, '11-11-2022', 500, 'T-Shirt', 1, 500, 1, 0, 0, '', 0),
(5, 'gokul', 2, 0, '11-11-2022', 1000, 'Shoes', 3, 3000, 0, 1, 1, 'rtshop', 0),
(6, 'gokul', 4, 0, '11-11-2022', 500, 'T-Shirt', 0, 0, 0, 0, 0, 'rrtextile', 0);

-- --------------------------------------------------------

--
-- Table structure for table `rt_category`
--

CREATE TABLE `rt_category` (
  `id` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_category`
--

INSERT INTO `rt_category` (`id`, `retailer`, `category`) VALUES
(1, 'rtshop', 'Men-Shirt'),
(2, 'rtshop', 'Shoes'),
(3, 'rrtextile', 'Men-Shirt'),
(4, 'rrtextile', 'Camera'),
(5, 'rrtextile', 'Watch');

-- --------------------------------------------------------

--
-- Table structure for table `rt_customer`
--

CREATE TABLE `rt_customer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `otp` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_customer`
--

INSERT INTO `rt_customer` (`id`, `name`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `otp`) VALUES
(1, 'Gokul', '4/6, 3rd cross, MK Nagar', 'Salem', 8621459855, 'gokul@gmail.com', 'gokul', '1234', '10-11-2022', '8307'),
(2, 'Vijay', '5/1', 'Karur', 7354245248, 'rndittrichy@gmail.com', 'vijay', '1234', '11-11-2022', '9259');

-- --------------------------------------------------------

--
-- Table structure for table `rt_employee`
--

CREATE TABLE `rt_employee` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `city` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_employee`
--

INSERT INTO `rt_employee` (`id`, `name`, `retailer`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `status`) VALUES
(1, 'Ram', 'rtshop', 'Salem', 8896577415, 'ram@gmail.com', 'E001', '123456', '15-04-2023', 0);

-- --------------------------------------------------------

--
-- Table structure for table `rt_product`
--

CREATE TABLE `rt_product` (
  `id` int(11) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `category` varchar(50) NOT NULL,
  `product` varchar(100) NOT NULL,
  `price` double NOT NULL,
  `quantity` int(11) NOT NULL,
  `photo` varchar(50) NOT NULL,
  `details` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `required_qty` int(11) NOT NULL,
  `scount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_product`
--

INSERT INTO `rt_product` (`id`, `retailer`, `category`, `product`, `price`, `quantity`, `photo`, `details`, `status`, `required_qty`, `scount`) VALUES
(1, 'rtshop', 'Men-Shirt', 'T-Shirt', 455, 108, 'P1product-2.jpg', 'Men T-Shirt', 0, 0, 2),
(2, 'rtshop', 'Shoes', 'Shoes', 1000, 5, 'P2product-4.jpg', 'Shoes', 1, 7, 2),
(3, 'rtshop', 'Shoes', 'Shoe', 950, 30, 'P3cat-3.jpg', 'Shoe', 0, 0, 0),
(4, 'rrtextile', 'Men-Shirt', 'T-Shirt', 500, 4, 'P4product-2.jpg', 'Men T-Shirt', 1, 0, 1),
(5, 'rrtextile', 'Camera', 'Digital Camera', 15000, 50, 'P5product-1.jpg', 'Digital Camera', 0, 0, 0),
(6, 'rrtextile', 'Watch', 'Smart Watch', 5000, 10, 'P6product-6.jpg', 'Smart Watch with Blue Thooth', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `rt_purchase`
--

CREATE TABLE `rt_purchase` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `amount` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_purchase`
--

INSERT INTO `rt_purchase` (`id`, `uname`, `amount`, `rdate`) VALUES
(1, 'vijay', 500, '11-11-2022'),
(2, 'gokul', 2910, '11-11-2022');

-- --------------------------------------------------------

--
-- Table structure for table `rt_retailer`
--

CREATE TABLE `rt_retailer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rt_retailer`
--

INSERT INTO `rt_retailer` (`id`, `name`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `status`) VALUES
(1, 'RT Shop', '65/1, Big Bazar', 'Trichy', 9517624693, 'rndittrichy@gmail.com', 'rtshop', '1234', '08-11-2022', 1),
(2, 'RR Textile', '4/7', 'Karur', 7354245248, 'rndittrichy@gmail.com', 'rrtextile', '1234', '11-11-2022', 1);
