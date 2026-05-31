import os

file_path = "/Users/andreasmuller/experiments/cernsim/CERN_Visualisierung/scripts/create_notebook.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

# Find the start index
start_idx = -1
for idx, line in enumerate(lines):
    if "// Check if ready for ramping" in line and idx + 1 < len(lines) and "const targetE=" in lines[idx+1]:
        start_idx = idx
        break

if start_idx != -1:
    print(f"Found start index: {start_idx}")
    
    # Find the end index
    end_idx = -1
    for idx in range(start_idx + 10, min(start_idx + 60, len(lines))):
        if "setStatus" in lines[idx] and "RAMPING BEENDET" in lines[idx] and idx + 1 < len(lines) and "});" in lines[idx+1]:
            end_idx = idx + 1
            break
            
    if end_idx != -1:
        print(f"Found end index: {end_idx}")
        
        # Corrected replacement code block
        corrected_replacement = """  // Check if ready for ramping
  if(b1Count>=NEEDED && b2Count>=NEEDED && !ramped){
   btnRamp.classList.remove("off");
   setStatus("LHC GEFÜLLT — Ramping möglich!","on");
  } else {
   setStatus("LHC B1:"+b1Count+"/"+NEEDED+" B2:"+b2Count+"/"+NEEDED,"on");
  }

  injecting=false;
  btnB1.classList.remove("off"); btnB2.classList.remove("off");
  trSteps.forEach(s=>s.classList.remove("cur","cur-i","done"));
 }
}

// ═══════════════════════════════════════════════════════════════════════════
// LHC RAMPING
// ═══════════════════════════════════════════════════════════════════════════
btnRamp.addEventListener("click",async()=>{
 if(ramped||injecting||cryoRecovery) return;
 btnRamp.classList.add("off"); btnB1.classList.add("off"); btnB2.classList.add("off"); btnAuto.classList.add("off");
 sliEnergy.disabled = true; sliIntensity.disabled = true; sliRampSpeed.disabled = true;
 
 setStatus("RAMPING MAGNETFELD & ENERGIE...","on");
 
 const startE=isIon?177:450;
 const targetE=paramEnergy*1000; // to GeV
 const startSpeed=0.0015;
 const targetSpeed=0.007 * (paramEnergy / 6.8);
 
 // Ramprate bestimmt die Dauer (höhere dB/dt = schnelleres Ramping)
 const dur = 200 / paramRampSpeed;
 let t0=null;
 let quenched = false;
 
 await new Promise(res=>{
  function step(ts){
   if(!t0) t0=ts;
   let p=Math.min((ts-t0)/dur,1);
   
   // Quench Schutz: Wenn dB/dt > 0.10 T/s, detektieren wir nach 40% des Weges einen Quench!
   if(paramRampSpeed > 0.10 && p > 0.40) {
    quenched = true;
    res();
    return;
   }
   
   lhcEnergy=startE+p*(targetE-startE);
   lhcSpeed=startSpeed+p*(targetSpeed-startSpeed);
   rbar.style.width=(p*100)+"%";
   updateReadouts();
   p<1 ? requestAnimationFrame(step) : res();
  }
  requestAnimationFrame(step);
 });
 
 if(quenched) {
  triggerQuench();
  return;
 }
 
 ramped=true;
 btnSqueeze.classList.remove("off");
 sliBeta.disabled = false;
 setStatus("RAMPING BEENDET — Squeeze-Phase einleiten!","on");
});"""
        
        new_lines = lines[:start_idx] + [corrected_replacement] + lines[end_idx+1:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        print("Successfully patched create_notebook.py!")
    else:
        print("Could not find end index!")
else:
    print("Could not find start index!")
