let staticLink
if (window.location.href.includes("http://localhost:3000/")) {
  staticLink = "/img/"
} else {
  staticLink = "/static/img/"
}
export default staticLink