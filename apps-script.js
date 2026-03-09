// ============================================================
// COLE ESTE CÓDIGO NO GOOGLE APPS SCRIPT
// Planilha: https://docs.google.com/spreadsheets/d/1Ox7r0lEO2ATI9UJr4ttb1IskkqhiGDThtWipDwOsT78
//
// Como fazer:
//  1. Abra a planilha → Extensions → Apps Script
//  2. Apague o código existente e cole tudo abaixo
//  3. Salve (Ctrl+S)
//  4. Clique em "Deploy" → "New deployment"
//  5. Tipo: "Web app"
//     - Execute as: "Me"
//     - Who has access: "Anyone"
//  6. Clique "Deploy" e copie a URL gerada
//  7. Cole a URL no index.html onde está: COLE_AQUI_A_URL_DO_APPS_SCRIPT
// ============================================================

var SHEET_ID = '1Ox7r0lEO2ATI9UJr4ttb1IskkqhiGDThtWipDwOsT78';
var ABA      = 'Confirmações'; // nome da aba na planilha (crie com este nome ou mude aqui)

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);
    var nome      = dados.nome      || '';
    var presenca  = dados.presenca  || '';
    var convidados = dados.convidados || '1';

    var ss  = SpreadsheetApp.openById(SHEET_ID);
    var aba = ss.getSheetByName(ABA);

    // Cria a aba e o cabeçalho se não existir
    if (!aba) {
      aba = ss.insertSheet(ABA);
      aba.appendRow(['Data/Hora', 'Nome', 'Presença em', 'Nº de pessoas']);
      aba.getRange(1, 1, 1, 4).setFontWeight('bold');
    }

    var agora = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
    aba.appendRow([agora, nome, presenca, convidados]);

    return ContentService
      .createTextOutput(JSON.stringify({result: 'ok'}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch(err) {
    return ContentService
      .createTextOutput(JSON.stringify({result: 'error', msg: err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Teste manual: Execute esta função no editor para verificar se a planilha abre corretamente
function testar() {
  var ss  = SpreadsheetApp.openById(SHEET_ID);
  Logger.log('Planilha: ' + ss.getName());
}
