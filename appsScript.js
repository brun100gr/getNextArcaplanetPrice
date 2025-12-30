function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const nuovoPrezzo = Number(data.prezzo);

    const sheet = SpreadsheetApp
      .getActiveSpreadsheet()
      .getSheets()[0];

    const lastRow = sheet.getLastRow();

    // Prima riga (solo intestazione)
    if (lastRow < 2) {
      sheet.appendRow([new Date(), nuovoPrezzo]);
      return ok("Prima riga inserita");
    }

    const lastDate  = sheet.getRange(lastRow, 1).getValue();
    const lastPrice = Number(sheet.getRange(lastRow, 2).getValue());

    const today = new Date();
    const sameDay = isSameDay(today, lastDate);

    // 🔁 STESSO GIORNO
    if (sameDay) {
      if (nuovoPrezzo === lastPrice) {
        return ok("Prezzo invariato");
      }

      const cell = sheet.getRange(lastRow, 2);

      // ⚠️ colore PRIMA, valore DOPO
      colora(cell, nuovoPrezzo, lastPrice);
      cell.setValue(nuovoPrezzo);

      SpreadsheetApp.flush();
      return ok("Prezzo aggiornato oggi");
    }

    // 🆕 NUOVO GIORNO
    sheet.appendRow([today, nuovoPrezzo]);
    const newLastRow = sheet.getLastRow();
    const cell = sheet.getRange(newLastRow, 2);

    colora(cell, nuovoPrezzo, lastPrice);
    SpreadsheetApp.flush();

    return ok("Nuovo giorno, riga aggiunta");

  } catch (err) {
    return ContentService
      .createTextOutput("ERROR: " + err)
      .setMimeType(ContentService.MimeType.TEXT);
  }
}

function colora(cell, nuovo, precedente) {
  cell.setBackground(null); // reset

  if (nuovo > precedente) {
    cell.setBackground("#f4cccc"); // 🟥 rosso chiaro
  } else if (nuovo < precedente) {
    cell.setBackground("#d9ead3"); // 🟢 verde chiaro
  }
}

function isSameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
         d1.getMonth() === d2.getMonth() &&
         d1.getDate() === d2.getDate();
}

function ok(msg) {
  return ContentService
    .createTextOutput("OK: " + msg)
    .setMimeType(ContentService.MimeType.TEXT);
}
