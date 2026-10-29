'use strict';
const token=document.querySelector('meta[name="logicasophia-token"]').content;
const $=(id)=>document.getElementById(id);
let current=null, polling=null;
const api=async(url, options={})=>{
 const response=await fetch(url,{cache:'no-store',...options});
 const data=await response.json();
 if(!response.ok)throw new Error(data.error||`HTTP ${response.status}`);
 return data;
};
const showError=(msg)=>{$('run-error').hidden=!msg;$('run-error').textContent=msg||'';};
const createNode=(name, text, css)=>{const el=document.createElement(name);if(text!==undefined)el.textContent=text;if(css)el.className=css;return el;};
async function status(){
 try{
  const doc=await api('/api/status');
  $('model-status').textContent=doc.backend_ready?'Connected · Ready':'Backend offline';
  $('backend-detail').textContent=doc.backend_ready?'Local inference active':(doc.backend_error||'Start model server :8090');
  $('workspace').textContent=doc.workspace;
  const sel=$('model'),selected=sel.value;sel.replaceChildren();
  if(doc.models.length){for(const name of doc.models){const opt=createNode('option',name);opt.value=name;sel.append(opt)}if(doc.models.includes(selected))sel.value=selected;}
  else{const opt=createNode('option','No loaded model');opt.value='';sel.append(opt)}
  $('run').disabled=!doc.backend_ready||!!current;
 }catch(err){showError(err.message);$('run').disabled=true;}
}
function traceEvents(events){
 const parent=$('trace');parent.replaceChildren();
 if(!events.length){parent.append(createNode('p','Waiting for first model decision…','muted'));return}
 for(const e of events){
  const item=createNode('div',undefined,'trace-item');
  item.append(createNode('span','', 'dot'));
  const content=createNode('div',undefined,'trace-content');
  const name=e.type==='state'?`State · ${e.state}`:e.type==='decision'?`Model · ${e.action}`:e.type==='evidence'?`Observed · ${e.action}`:e.type==='verification'?'Evidence rechecked':String(e.type);
  content.append(createNode('b',name));
  if(e.path)content.append(createNode('small',e.path));
  if(e.result)content.append(createNode('small',e.result));
  item.append(content);parent.append(item);
 }
 parent.scrollTop=parent.scrollHeight;
}
function resultPane(run){
 const node=$('result');node.replaceChildren();
 if(run.error){node.append(createNode('p',run.error,'error'));return}
 const r=run.result;
 if(!r){node.append(createNode('p','The local model is processing the task.','muted'));return}
 node.append(createNode('div',r.answer||'No final answer produced.','answer'));
 const evidence=createNode('div',undefined,'evidence');
 for(const proof of (r.evidence||[])){const ref=proof.path||'(unknown)';evidence.append(createNode('span',`${proof.action||proof.tool}: ${ref}`));}
 node.append(evidence);
 node.append(createNode('div',`Status: ${r.status} · Model calls: ${r.model_calls} · Time: ${r.elapsed_seconds}s · Verification: source integrity only`,'details'));
 node.append(createNode('p',`Audit: ${r.directory}`,'details'));
 if(r.reason)node.append(createNode('p',`Reason: ${r.reason}`,'error'));
}
async function refreshRuns(){
 try{const doc=await api('/api/runs'); const list=$('history');list.replaceChildren();
  if(!doc.runs.length){list.append(createNode('span','No tasks yet','muted'));return}
  for(const row of doc.runs.slice(0,9)){
   const b=createNode('button',row.goal,'history-item');
   b.append(createNode('small',row.status));b.addEventListener('click',()=>watch(row.run_id));list.append(b);
  }
 }catch(_err){}
}
async function watch(id){
 if(polling){clearInterval(polling);polling=null}
 current=id; await tick(); polling=setInterval(tick,900);
}
async function tick(){
 if(!current)return;
 try{
  const run=await api(`/api/runs/${current}`);
  $('run-state').textContent=run.status;
  traceEvents(run.events||[]);resultPane(run);
  if(!['QUEUED','RUNNING'].includes(run.status)){
   clearInterval(polling);polling=null;current=null;await refreshRuns();await status();
  }
 }catch(err){clearInterval(polling);polling=null;current=null;showError(err.message);await status();}
}
$('run').addEventListener('click',async()=>{
 showError('');const goal=$('goal').value.trim(); if(!goal){showError('Enter an engineering task.');return}
 $('run').disabled=true;
 try{
  const doc=await api('/api/runs',{method:'POST',headers:{'Content-Type':'application/json','X-LogicaSophia-Token':token},
   body:JSON.stringify({goal,model:$('model').value||null})});
  await watch(doc.run_id);await refreshRuns();
 }catch(err){showError(err.message);await status();}
});
status();refreshRuns();setInterval(()=>{if(!current)status()},12000);
