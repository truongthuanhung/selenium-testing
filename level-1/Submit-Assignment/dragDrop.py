import os
from selenium.webdriver.common.by import By

def drop_file(paths: list[str], target_element, driver):
    # Validate file paths
    for path in paths:
        if not os.path.isfile(path):
            raise ValueError(f"{path} is not a valid file path.")

    # Get the target element ID
    target_id = target_element.get_attribute("id")

    # Add an ID if the target doesn't have one
    if not target_id:
        target_id = "seleniumDragAndDropInput_target"
        driver.execute_script("arguments[0].id = arguments[1];", target_element, target_id)

    # Create form and inputs
    create_inputs_script = """
        var f = document.createElement('form');
        f.setAttribute('id', 'seleniumDragAndDropInput_form');
        f.setAttribute('style', 'position: fixed; left: 0; top: 0; width: 100px; height: 100px;');
        document.body.appendChild(f);
    """
    for i, path in enumerate(paths):
        create_inputs_script += f"""
            var input{i} = document.createElement('input');
            input{i}.setAttribute('type', 'file');
            input{i}.setAttribute('id', 'seleniumDragAndDropInput{i}');
            document.getElementById('seleniumDragAndDropInput_form').appendChild(input{i});
        """
    driver.execute_script(create_inputs_script)

    # Set file for each input
    for i, path in enumerate(paths):
        input_element = driver.find_element(By.ID, f"seleniumDragAndDropInput{i}")
        input_element.send_keys(path)

    # Init event with files
    gather_inputs_script = """
        var seleniumDragAndDropFiles = [];
        seleniumDragAndDropFiles.item = function(i) { return seleniumDragAndDropFiles[i]; };
    """
    for i in range(len(paths)):
        gather_inputs_script += f"seleniumDragAndDropFiles.push(document.getElementById('seleniumDragAndDropInput{i}').files[0]);"
    dispatch_event_script = """
        var eve = document.createEvent('HTMLEvents');
        eve.initEvent('drop', true, true);
        eve.dataTransfer = { files: seleniumDragAndDropFiles };
        eve.type = 'drop';
        document.getElementById(arguments[0]).dispatchEvent(eve);
    """
    driver.execute_script(gather_inputs_script + dispatch_event_script, target_id)

    # Cleanup
    driver.execute_script("document.getElementById('seleniumDragAndDropInput_form').remove();")
    if target_id == "seleniumDragAndDropInput_target":
        driver.execute_script("document.getElementById('seleniumDragAndDropInput_target').removeAttribute('id');")

