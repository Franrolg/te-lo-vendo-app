document.addEventListener("change", detalleCompra, false);

function detalleCompra(evento) {
  let prodcutoId, cantidadProductos;

  if (evento.target) {
    prodcutoId = evento.target.id, cantidadProductos = evento.target.value;
  } else {
    prodcutoId = evento.id, cantidadProductos = evento.value;
  }

  let datosProducto = document.getElementById(prodcutoId).parentElement.parentElement.parentElement;
  let productoDetalle = document.getElementById("cantidad-" + prodcutoId);

  if (!productoDetalle) {
    crearTarjeta(datosProducto.getElementsByTagName('img')[0].attributes.src.value,
      datosProducto.getElementsByClassName('precio')[0].innerText,
      cantidadProductos, prodcutoId, datosProducto.getElementsByClassName('nombre')[0].innerText);

  } else if (cantidadProductos == 0) {
    mostrarDetalle(prodcutoId, true);
  } else {
    mostrarDetalle(prodcutoId, false);
    productoDetalle.value = cantidadProductos;
  }
}

function mostrarDetalle(productoId, mostrar) {
  let detalles = document.getElementsByClassName("detalle-" + productoId)
  for (var key in detalles) detalles[key].hidden = mostrar;
}

function crearTarjeta(imgProducto, precioProducto, cantidadProducto, productoId, productoNombre) {
  /* Función para crear tarjeta de detalle en el "carrito de compras" */
  const claseProducto = "detalle-" + productoId;

  let carritoCompras = document.getElementById('carrito-compras'); // Elemento donde se colocarán los detalles

  /* DIV con la imagen del auto */
  let divImg = crearElemento('div', 'col-md-2 col-4 mt-2 ' + claseProducto);
  divImg.appendChild(crearElemento('img', 'img-fluid rounded-start detail-image ' + claseProducto, { 'src': imgProducto }));
  carritoCompras.appendChild(divImg);

  /* DIV con el detalle del auto y compra */
  let cardBody = crearElemento('div', 'card-body ' + claseProducto);
  let tituloBody = crearElemento('h5', 'card-tittle ' + claseProducto, null, productoNombre);
  let parrafoBody = crearElemento('p', 'card-text justify-content-center ' + claseProducto, null, "Precio unitario: " + precioProducto);

  tituloBody.appendChild(crearElemento('input', claseProducto, { 'type': "number", "name": productoId, 'id': "cantidad-" + productoId, "value": cantidadProducto }));

  cardBody.appendChild(tituloBody);
  cardBody.appendChild(parrafoBody);

  let divDetalle = crearElemento('div', 'col-md-4 col-8 ' + claseProducto);
  divDetalle.appendChild(cardBody);
  carritoCompras.appendChild(divDetalle);
}

function crearElemento(elemento, clases, atributos, texto) {
  let elementoCreado = document.createElement(elemento);
  elementoCreado.className = clases;
  if (atributos) for (var key in atributos) elementoCreado.setAttribute(key, atributos[key]);
  if (texto) elementoCreado.innerText = texto;

  return elementoCreado;
}

function sumar(evento) {

  if (evento) {
    let clasesEvento = evento.target.className;
    let inputValor = evento.target.parentElement.getElementsByTagName('input')[0];
    let valorActual = parseInt(inputValor.value);

    if (clasesEvento.indexOf('sumar') >= 0) valorActual += 1;
    if (clasesEvento.indexOf('restar') >= 0) valorActual -= 1;

    if (valorActual >= 0 && valorActual <= 10) inputValor.value = valorActual, detalleCompra(inputValor);

  }


  var productosTotal = 0, montoTotal = 0, sku = "SKU00";
  for (let index = 1; index <= 20; index++) {
    if (index > 9) sku = "SKU0";
    let cantidadProducto = parseInt(document.getElementById(sku + index).value);
    let precioProducto = parseInt(document.getElementById('precio-' + sku + index).innerText.slice(1))

    productosTotal += cantidadProducto;
    montoTotal += (precioProducto * cantidadProducto);
  }

  document.getElementById("resultado").innerText = productosTotal;
  document.getElementById("total-compra").innerHTML = "<b>Monto Total </b> $" + montoTotal;


}


