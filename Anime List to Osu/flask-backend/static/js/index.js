function makePostRequest(animeList) {
  // const dynamicContentDiv = document.getElementById('dynamicContent');
  // const dynamicHTML = '<h1>Hello, this is dynamically generated HTML!</h1>' +
  //                     '<p>This content is created by calling a JavaScript function.</p>' +
  //                     '<img src="path/to/image.jpg" alt="Dynamic Image">';

  // // Set the content of the div to the dynamically generated HTML
  // dynamicContentDiv.innerHTML = dynamicHTML;
  console.log(animeList);
}

function clearList(inputString) {
  var listFormatted = inputString.split("Seperator_Tags");
  try {
    listFormatted[0] = listFormatted[0].replace("[&#39;", "");
  } catch (error) {
    console.log(error);
  }
  try {
    l = listFormatted.length - 1;
    listFormatted[l] = listFormatted[l].replace(
      ", &#39;&lt;Seperator_Tags&gt;&#39;]",
      ""
    );
  } catch (error) {
    console.log(error);
  }
  for (var i = 0; i < listFormatted.length; i++) {
    listFormatted[i] = listFormatted[i].replace("&#39;", "");
  }
  return listFormatted;
}
