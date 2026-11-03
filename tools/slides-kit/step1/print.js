// Print run-sheet: @media print hides the stage and prints number, title, frames with timing and notes.
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({});
  await page.emulateMedia({media:'print'});await L.wait(page,300);
  const info=await page.evaluate(()=>({stage:getComputedStyle(document.getElementById('stage')).display,sheet:getComputedStyle(document.getElementById('runsheet')).display,
    sections:document.querySelectorAll('#runsheet section').length,items:document.querySelectorAll('#runsheet li').length,text:document.getElementById('runsheet').innerText.slice(0,400)}));
  await page.screenshot({path:L.OUT+'/runsheet.png',fullPage:true});
  await page.pdf({path:L.OUT+'/runsheet.pdf',format:'Letter',printBackground:false});
  const pdf=require('fs').readFileSync(L.OUT+'/runsheet.pdf','latin1'),pages=(pdf.match(/\/Type\s*\/Page[^s]/g)||[]).length;
  const pass=info.stage==='none'&&info.sheet==='block'&&info.sections>0&&!errors.length;
  console.log(`print: ${pass?'PASS':'FAIL'} stage hidden=${info.stage==='none'}, ${info.sections} slides, ${info.items} frame lines, ${pages} PDF page(s)`);
  L.save('print.json',{...info,pages});
  await browser.close();process.exitCode=pass?0:1;
})();
