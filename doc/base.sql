create DATABASE if not EXISTS base;
USE `base`;
CREATE TABLE if not exists `usuario` (
  `idusuario` int AUTO_INCREMENT NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `direccion` varchar(30) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `email` varchar(30) UNIQUE NOT NULL,
  `clave` varchar(10) NOT NULL,
  PRIMARY KEY (`idusuario`)
);
CREATE TABLE if not exists `productos` (
  `idproducto` int AUTO_INCREMENT NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(1000) NOT NULL,
  `precio` int(30) NOT NULL,
  `stock` int(30) NOT NULL,
  `categoria` varchar(30) NOT NULL,
  `descuento` int(3) NOT NULL,
  `vendidos` int(30) NOT NULL,
  PRIMARY KEY (`idproducto`)
);
CREATE TABLE if not exists `imgproductos` (
  `idproducto` int(10) NOT NULL,
  `rutaimg` varchar(255) NOT NULL,
  FOREIGN KEY (`idproducto`) REFERENCES `productos`(`idproducto`) ON DELETE CASCADE
);

CREATE TABLE if not exists `carritos` (
  `idcarrito` int AUTO_INCREMENT NOT NULL,
  `idusuario` int(10) NOT NULL,
  `preciotot` int(30) NOT NULL,
  `comprado` VARCHAR(2) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`idcarrito`),
  FOREIGN KEY (`idusuario`) REFERENCES `usuario`(`idusuario`) ON DELETE CASCADE
);

CREATE TABLE if not exists `productoscarrito` (
  `idcarrito` int(10) NOT NULL,
  `idproducto` int(10) NOT NULL,
  `cantidad` int(10) NOT NULL,
  FOREIGN KEY (`idcarrito`) REFERENCES `carritos`(`idcarrito`) ON DELETE CASCADE,
  FOREIGN KEY (`idproducto`) REFERENCES `productos`(`idproducto`) ON DELETE CASCADE
);

CREATE TABLE if not exists `compras` (
  `idcompra` int AUTO_INCREMENT NOT NULL,
  `idusuario` int(10) NOT NULL,
  `idcarrito` int(10) NOT NULL,
  `tipoenvio` varchar(30) NOT NULL,
  `estadocompra` varchar(30) NOT NULL,
  PRIMARY KEY (`idcompra`),
  FOREIGN KEY (`idusuario`) REFERENCES `usuario`(`idusuario`) ON DELETE CASCADE,
  FOREIGN KEY (`idcarrito`) REFERENCES `carritos`(`idcarrito`) ON DELETE CASCADE
);

CREATE TABLE if not exists `chat` (
  `idchat` int AUTO_INCREMENT NOT NULL,
  `idusuario` int(10) NOT NULL,
  `idcompra` int(10) NULL,
  PRIMARY KEY (`idchat`),
  FOREIGN KEY (`idusuario`) REFERENCES `usuario`(`idusuario`) ON DELETE CASCADE,
  FOREIGN KEY (`idcompra`) REFERENCES `compras`(`idcompra`) ON DELETE CASCADE
);

CREATE TABLE if not exists `mensajes` (
  `idchat` int(10) NOT NULL,
  `idusuario` int(10) NOT NULL,
  `mensaje` varchar(200) NOT NULL,
  `fecha_hora` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`idchat`) REFERENCES `chat`(`idchat`) ON DELETE CASCADE,
  FOREIGN KEY (`idusuario`) REFERENCES `usuario`(`idusuario`) ON DELETE CASCADE
);