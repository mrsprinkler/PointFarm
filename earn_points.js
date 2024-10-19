console.error('OPENING NEW FROM')

const element = arguments[0]
console.log(element)
const PROMPT = element.parentElement.parentElement.children[2].innerText

if(element.id!=="locked_required_text"){
    console.error('Oppening:')
    element.click()
    console.error('Oppened')
}
return PROMPT