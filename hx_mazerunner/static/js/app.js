document.body.addEventListener("htmx:configRequest", (event) => {
  const {
    detail: { triggeringEvent, parameters, elt, path },
  } = event;
  if (path !== "/move") return;

  switch (triggeringEvent.code) {
    case "ArrowUp":
      parameters.direction = "N";
      break;
    case "ArrowDown":
      parameters.direction = "S";
      break;
    case "ArrowLeft":
      parameters.direction = "W";
      break;
    case "ArrowRight":
      parameters.direction = "E";
      break;
    default:
      break;
  }
  const [_, row, col] = elt.id.split("-");
  parameters.row = row;
  parameters.col = col;
});

