


function create_html_employee_hr_info(submission_data){
    const returnval= 
        "<dl>"
      +   "<dt>"
      +      "Employee name"
      +   "</dt>"
      +   "<dd>"
      +      submission_data.employee_name
      +   "</dd>" 
      + "</dl>";
   return returnval;
}



function create_html(submission_data){
    const section_data = [
        {
            title: "Employee HR data",
            render_func: create_html_employee_hr_info
        }
    ];
    const returnval =
          "<dl>"
        + section_data.map(v => {
            return "<dt><b>" + v.title + "</b></dt>"
              +"<dd>" + v.render_func(submission_data) + "</dd>"
        })
        + "</dl>";
    return returnval;

}

export {create_html};