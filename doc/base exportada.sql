-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-02-2025 a las 03:58:02
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `base`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carritos`
--

CREATE TABLE `carritos` (
  `idcarrito` int(11) NOT NULL,
  `idusuario` int(10) NOT NULL,
  `preciotot` int(30) NOT NULL,
  `comprado` varchar(2) NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carritos`
--

INSERT INTO `carritos` (`idcarrito`, `idusuario`, `preciotot`, `comprado`) VALUES
(2, 4, 0, 'no'),
(24, 7, 637500, 'sí'),
(25, 8, 546320, 'sí'),
(26, 3, 166100, 'sí'),
(27, 3, 245600, 'sí'),
(28, 8, 26320, 'sí'),
(29, 8, 1060200, 'sí'),
(31, 3, 320000, 'sí'),
(32, 9, 698240, 'sí'),
(33, 3, 101500, 'sí'),
(34, 3, 104500, 'sí'),
(35, 3, 173880, 'sí'),
(36, 3, 24500, 'sí'),
(37, 3, 26320, 'sí'),
(38, 3, 98400, 'sí'),
(39, 3, 39900, 'sí'),
(40, 3, 637500, 'sí'),
(41, 3, 24500, 'sí'),
(42, 3, 26320, 'sí'),
(43, 3, 104500, 'sí'),
(44, 9, 173880, 'sí'),
(45, 9, 24500, 'sí'),
(46, 9, 520000, 'sí'),
(47, 9, 104500, 'sí'),
(48, 8, 55040, 'sí');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `chat`
--

CREATE TABLE `chat` (
  `idchat` int(11) NOT NULL,
  `idusuario` int(10) NOT NULL,
  `idcompra` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `chat`
--

INSERT INTO `chat` (`idchat`, `idusuario`, `idcompra`) VALUES
(4, 7, NULL),
(5, 7, 22),
(6, 8, NULL),
(7, 8, 23),
(8, 3, 24),
(9, 3, 25),
(10, 8, 26),
(11, 8, 27),
(13, 3, 29),
(14, 9, NULL),
(15, 9, 30),
(16, 3, 31),
(17, 3, 32),
(18, 3, 33),
(19, 3, 34),
(20, 3, 35),
(21, 3, 36),
(22, 3, 37),
(23, 3, 38),
(24, 3, 39),
(25, 3, 40),
(26, 3, 41),
(27, 9, 42),
(28, 9, 43),
(29, 9, 44),
(30, 9, 45),
(31, 8, 46);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `idcompra` int(11) NOT NULL,
  `idusuario` int(10) NOT NULL,
  `idcarrito` int(10) NOT NULL,
  `tipoenvio` varchar(30) NOT NULL,
  `estadocompra` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`idcompra`, `idusuario`, `idcarrito`, `tipoenvio`, `estadocompra`) VALUES
(22, 7, 24, 'retiro', 'Pendiente de pago'),
(23, 8, 25, 'retiro', 'En proceso'),
(24, 3, 26, 'envio', 'Recibido'),
(25, 3, 27, 'envio', 'Recibido'),
(26, 8, 28, 'retiro', 'En proceso'),
(27, 8, 29, 'retiro', 'En proceso'),
(29, 3, 31, 'envio', 'En viaje'),
(30, 9, 32, 'envio', 'Pendiente de pago'),
(31, 3, 33, 'retiro', 'Pendiente de pago'),
(32, 3, 34, 'retiro', 'Pendiente de pago'),
(33, 3, 35, 'retiro', 'Pendiente de pago'),
(34, 3, 36, 'retiro', 'Pendiente de pago'),
(35, 3, 37, 'retiro', 'Pendiente de pago'),
(36, 3, 38, 'retiro', 'Pendiente de pago'),
(37, 3, 39, 'retiro', 'Pendiente de pago'),
(38, 3, 40, 'retiro', 'Pendiente de pago'),
(39, 3, 41, 'retiro', 'Pendiente de pago'),
(40, 3, 42, 'retiro', 'Pendiente de pago'),
(41, 3, 43, 'retiro', 'Pendiente de pago'),
(42, 9, 44, 'retiro', 'Pendiente de pago'),
(43, 9, 45, 'retiro', 'Pendiente de pago'),
(44, 9, 46, 'retiro', 'Pendiente de pago'),
(45, 9, 47, 'retiro', 'Pendiente de pago'),
(46, 8, 48, 'retiro', 'En proceso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imgproductos`
--

CREATE TABLE `imgproductos` (
  `idproducto` int(10) NOT NULL,
  `rutaimg` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imgproductos`
--

INSERT INTO `imgproductos` (`idproducto`, `rutaimg`) VALUES
(1, '1_7833781f8b624e659200abceabae3f0b.png'),
(5, '5_ffd7ce541eee4d0ca53739b5fe2e3552.png'),
(6, '6_d1e72b870c7e407f9a76428eb5fbd2b3.png'),
(2, '2_b0c8b08f8a4f48ba8ce5039bf6819fb0.png'),
(4, '4_30f845a0b6c64e76a7be5318e1c01e18.png'),
(3, '3_6f0e6074ca40471fa4a05ea7e16e27e6.png'),
(7, '7_19e6cb98947341bba4af5cbcd4bdc95d.png'),
(8, '8_2429302dd0b6453e80d1757f1852da79.png'),
(9, '9_23e244b5bb26423c85995084d73d35d5.png'),
(10, '10_9008f911b4ad4eebbe22547e445812f3.png'),
(11, '11_52a980bf138d45e1a6291ce459bb9caa.png'),
(12, '12_6086221e0488430785f27a871a5515f0.png'),
(13, '13_fe985f9cc6be46d9b6d118df77e0860e.png'),
(13, '13_0b66a652aebc46e8af1fd8465e9fcd67.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes`
--

CREATE TABLE `mensajes` (
  `idchat` int(10) NOT NULL,
  `idusuario` int(10) NOT NULL,
  `mensaje` varchar(200) NOT NULL,
  `fecha_hora` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensajes`
--

INSERT INTO `mensajes` (`idchat`, `idusuario`, `mensaje`, `fecha_hora`) VALUES
(4, 7, 'Ya compre?', '2025-02-11 16:37:58'),
(5, 7, 'por aca te aviso el pago?', '2025-02-11 16:38:06'),
(5, 1, 'claro', '2025-02-11 16:39:00'),
(4, 1, 'si', '2025-02-11 17:14:41'),
(6, 8, 'hola tenes cpu', '2025-02-11 17:31:34'),
(7, 8, 'pague', '2025-02-11 17:32:00'),
(6, 1, 'tenemos', '2025-02-11 17:37:34'),
(7, 1, 'ok', '2025-02-11 17:37:46'),
(8, 3, 'pague', '2025-02-11 17:42:17'),
(8, 3, 'cuando llega?', '2025-02-11 17:42:24'),
(10, 8, 'pague', '2025-02-12 19:09:06'),
(11, 8, 'pague', '2025-02-12 19:09:18'),
(11, 1, 'ok', '2025-02-12 19:13:51'),
(10, 1, 'ok', '2025-02-12 19:14:00'),
(8, 1, 'ok, en 5 dias', '2025-02-12 19:14:16'),
(10, 1, 'aa', '2025-02-13 12:30:39'),
(10, 1, 'aaaaa', '2025-02-13 12:30:43'),
(10, 1, 'aaaaaa', '2025-02-13 12:30:47'),
(5, 1, 'Null', '2025-02-13 12:44:09'),
(5, 1, 'null', '2025-02-13 12:44:14'),
(5, 1, '#null', '2025-02-13 12:44:22'),
(5, 1, '#Null', '2025-02-13 12:44:29'),
(5, 1, '«… y 1=1»', '2025-02-13 12:45:55'),
(5, 1, '1=1', '2025-02-13 12:46:03'),
(5, 1, '<<>>', '2025-02-13 12:46:10'),
(5, 1, '0', '2025-02-13 12:46:35'),
(8, 3, 'ok', '2025-02-13 13:11:36'),
(13, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 13:36:46'),
(13, 3, 'ya pague!', '2025-02-13 13:39:39'),
(14, 9, 'que bueno que funciona!', '2025-02-13 17:26:56'),
(15, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 17:28:50'),
(16, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:03'),
(17, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:11'),
(18, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:18'),
(19, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:23'),
(20, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:28'),
(21, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:34'),
(22, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:40'),
(23, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:50'),
(24, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:47:56'),
(25, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:48:01'),
(26, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:48:10'),
(27, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:49:24'),
(28, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:49:29'),
(29, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:49:34'),
(30, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 20:49:40'),
(31, 1, '¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.', '2025-02-13 22:19:50'),
(31, 8, 'pague', '2025-02-13 22:20:13'),
(6, 8, 'cuando me lo envian?', '2025-02-13 22:20:39'),
(31, 8, 'cuando me lo mandan?', '2025-02-13 22:21:04'),
(6, 1, 'hablame por el chat de tu compra', '2025-02-13 22:23:55'),
(31, 1, 'en breve', '2025-02-13 22:24:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idproducto` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(1000) NOT NULL,
  `precio` int(30) NOT NULL,
  `stock` int(30) NOT NULL,
  `categoria` varchar(30) NOT NULL,
  `descuento` int(3) NOT NULL,
  `vendidos` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`idproducto`, `nombre`, `descripcion`, `precio`, `stock`, `categoria`, `descuento`, `vendidos`) VALUES
(1, 'Intel Core I3', 'Microprocesador', 145000, 20, 'Procesadores', 30, 12),
(2, 'SSD 480gb Adata', 'Disco de estado sólido', 32000, 41, 'Almacenamiento SSD', 14, 49),
(3, '4060 ti 16gb MSI', 'Placa de video de 16gb', 650000, 2, 'Placas de video', 20, 13),
(4, '4080 super 16gb MSI', 'Placa de video de 16gb', 850000, 1, 'Placas de video', 10, 5),
(5, '4070 super 12gb Asus', 'Placa de video de 12gb', 750000, 11, 'Placas de video', 15, 14),
(6, 'SSD 512gb T-Force', 'Disco de estado sólido', 42000, 10, 'Almacenamiento SSD', 5, 7),
(7, 'SSD NVMe 2tb Patriot', 'SSD NVMe M.2', 124000, 15, 'Almacenamiento SSD', 0, 8),
(8, 'SSD NVMe 4tb Adata', 'SSD NVMe M.2', 280000, 6, 'Almacenamiento SSD', 9, 3),
(9, 'HDD 4tb Seagate', 'Disco duro', 110000, 16, 'Almacenamiento HDD', 5, 25),
(10, 'HDD 8tb Seagate', 'Disco duro', 189000, 10, 'Almacenamiento HDD', 8, 7),
(11, 'DDR4 8gb Patriot Viper', 'Memoria RAM DDR4 de 8gb', 25000, 76, 'Memorias RAM', 2, 132),
(12, 'DDR4 8gb Asus Vulcan', 'Memoria RAM DDR4 de 8gb', 28000, 126, 'Memorias RAM', 6, 192),
(13, 'MSI Pro B760M-E DDR4', 'Motherboard para procesadores Intel DDR4', 120000, 10, 'Motherboards', 18, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productoscarrito`
--

CREATE TABLE `productoscarrito` (
  `idcarrito` int(10) NOT NULL,
  `idproducto` int(10) NOT NULL,
  `cantidad` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productoscarrito`
--

INSERT INTO `productoscarrito` (`idcarrito`, `idproducto`, `cantidad`) VALUES
(2, 3, 1),
(24, 5, 1),
(25, 3, 1),
(25, 12, 1),
(26, 6, 4),
(27, 1, 1),
(27, 2, 5),
(28, 12, 1),
(29, 4, 1),
(29, 13, 3),
(31, 9, 3),
(32, 1, 5),
(32, 12, 7),
(33, 1, 1),
(34, 9, 1),
(35, 10, 1),
(36, 11, 1),
(37, 12, 1),
(38, 13, 1),
(39, 6, 1),
(40, 5, 1),
(41, 11, 1),
(42, 12, 1),
(43, 9, 1),
(44, 10, 1),
(45, 11, 1),
(46, 3, 1),
(47, 9, 1),
(48, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idusuario` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `direccion` varchar(30) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `clave` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idusuario`, `nombre`, `direccion`, `telefono`, `email`, `clave`) VALUES
(1, 'Administrador', 'administrador', '11223344', 'a@a.a', 'admin'),
(2, 'Adamo', 'casa', '1122904476', 'adamonemcek@gmail.com', 'hola'),
(3, 'Hola', 'no te digo donde vivo', '11224455', 'hola@hola.com', 'hola'),
(4, 'renata', 'alsina 259', '1162199978', 'gonzalezrenata0406@gmail.com', '12345678'),
(7, 'Carlos Perez', 'carlitos 412', '454578454', 'carlos@gmail.com', 'hola'),
(8, 'Ana Maria', 'Pueyrredon', '1135653072', 'anamanicoletti@gmail.com', 'hola'),
(9, 'Adamo', 'Pueyrredon', '1122904476', 'yo@yo.com', 'hola');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD PRIMARY KEY (`idcarrito`),
  ADD KEY `idusuario` (`idusuario`);

--
-- Indices de la tabla `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`idchat`),
  ADD KEY `idusuario` (`idusuario`),
  ADD KEY `idcompra` (`idcompra`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`idcompra`),
  ADD KEY `idusuario` (`idusuario`),
  ADD KEY `idcarrito` (`idcarrito`);

--
-- Indices de la tabla `imgproductos`
--
ALTER TABLE `imgproductos`
  ADD KEY `idproducto` (`idproducto`);

--
-- Indices de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD KEY `idchat` (`idchat`),
  ADD KEY `idusuario` (`idusuario`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idproducto`);

--
-- Indices de la tabla `productoscarrito`
--
ALTER TABLE `productoscarrito`
  ADD KEY `idcarrito` (`idcarrito`),
  ADD KEY `idproducto` (`idproducto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idusuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carritos`
--
ALTER TABLE `carritos`
  MODIFY `idcarrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `chat`
--
ALTER TABLE `chat`
  MODIFY `idchat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `idcompra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `idproducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idusuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD CONSTRAINT `carritos_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`idcompra`) REFERENCES `compras` (`idcompra`) ON DELETE CASCADE;

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`idcarrito`) REFERENCES `carritos` (`idcarrito`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imgproductos`
--
ALTER TABLE `imgproductos`
  ADD CONSTRAINT `imgproductos_ibfk_1` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproducto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD CONSTRAINT `mensajes_ibfk_1` FOREIGN KEY (`idchat`) REFERENCES `chat` (`idchat`) ON DELETE CASCADE,
  ADD CONSTRAINT `mensajes_ibfk_2` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `productoscarrito`
--
ALTER TABLE `productoscarrito`
  ADD CONSTRAINT `productoscarrito_ibfk_1` FOREIGN KEY (`idcarrito`) REFERENCES `carritos` (`idcarrito`) ON DELETE CASCADE,
  ADD CONSTRAINT `productoscarrito_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproducto`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
