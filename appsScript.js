function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const newPrice = Number(data.prezzo);

    const sheet = SpreadsheetApp
      .getActiveSpreadsheet()
      .getSheets()[0];

    const lastRow = sheet.getLastRow();

    // First row (header only)
    if (lastRow < 2) {
      sheet.appendRow([new Date(), newPrice]);
      return ok("First row inserted");
    }

    const lastDate = sheet.getRange(lastRow, 1).getValue();
    const lastPrice = Number(sheet.getRange(lastRow, 2).getValue());

    const today = new Date();
    const sameDay = isSameDay(today, lastDate);

    // 🔄 SAME DAY
    if (sameDay) {
      if (newPrice === lastPrice) {
        return ok("Price unchanged");
      }

      const cell = sheet.getRange(lastRow, 2);

      // ⚠️ Color FIRST, value AFTER
      colorCell(cell, newPrice, lastPrice);
      cell.setValue(newPrice);

      SpreadsheetApp.flush();
      return ok("Price updated today");
    }

    // 🆕 NEW DAY
    sheet.appendRow([today, newPrice]);
    const newLastRow = sheet.getLastRow();
    const cell = sheet.getRange(newLastRow, 2);

    colorCell(cell, newPrice, lastPrice);
    SpreadsheetApp.flush();

    return ok("New day, row added");

  } catch (err) {
    return ContentService
      .createTextOutput("ERROR: " + err)
      .setMimeType(ContentService.MimeType.TEXT);
  }
}

function colorCell(cell, newPrice, previousPrice) {
  cell.setBackground(null); // reset

  if (newPrice > previousPrice) {
    cell.setBackground("#f4cccc"); // 🔴 light red
  } else if (newPrice < previousPrice) {
    cell.setBackground("#d9ead3"); // 🟢 light green
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
