const display=document.querySelector(".display");
const buttons=document.querySelectorAll("button");
const specialchar=["%","*","/","-","+","="];

let output="";

//define function to caculate based on button clicked.
const calculate=(btnValue)=>{

    if(btnValue==="="&&btnValue!==""){
        //if o/p has % replace with /100 before evalvating
        output=eval(output.replace("%","/100"));
    }
    else if(btnValue==="AC")
    {
        output="";
    }
    else if(btnValue==="DEL")
    {
        //if del button clicked, remove the last character from the o/p
        output=output.toString().slice(0,-1);
    }
    else{
        if(output==="" && specialchar.includes(btnValue))
            return;
        output += btnValue;
    }
     display.value=output;   
}
//add event listener to button,call calculate() on click

buttons.forEach((button)=>{
//button click listener calls calculate() with dataset val as argument
button.addEventListener("click", (e) =>calculate(e.target.dataset.value));
});
