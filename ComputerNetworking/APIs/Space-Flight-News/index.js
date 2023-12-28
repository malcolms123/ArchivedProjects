// defining endpoint
let baseUrl = "https://api.spaceflightnewsapi.net/v4/"
let endUrl = "?format=json"

// grabbing html elements
let pageDescription = document.getElementById("pageDescription")
let newsList = document.getElementById("newsList")
let summary = document.getElementById("summary")
let switchButton = document.getElementById("switchButton")

// initializing global variable to track content type
var contentType = "articles"

function getNews() {
	var url = baseUrl + contentType + endUrl

	console.log("making fetch to", url)
	
	fetch(url)
		.then(resp=>{return resp.json()})
		.then(json=>{
			// getting all results
			results = json.results
			console.log(`${results.length} ${contentType} found.`)
			
			// clearing html list to edit
			newsList.innerHTML = ""

			// populating list with json result
			results.forEach(result => {
				let li = document.createElement("li")
				li.appendChild(document.createTextNode(result.title))
				// listening for clicks on item
				li.addEventListener("click", function() { getSummary(result) })
				newsList.append(li)
			});

		})

}

// showing the summary
function getSummary(result) {
	console.log(`Showing summary of ${result.title}.`)
	summary.innerHTML = result.summary
}

function switchType() {
	// changing button
	switchButton.innerHTML = `Switch to ${contentType}`
	// switching type of content
	if (contentType == "articles") {
		contentType = "blogs"
	} else if (contentType == "blogs"){
		contentType = "reports"
	} else {
		contentType = "articles"
	}
	console.log(`Switching to ${contentType}`)
	// changing page description
	pageDescription.innerHTML = `A list of some space ${contentType} as provided by the <i>Space Flight News</i> API`
	// clearing summary
	summary.innerHTML = ""
	// pulling news again
	getNews()
}

document.addEventListener("DOMContentLoaded", () => {
  getNews()
});
