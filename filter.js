function filterByCategory(category) {
    const articles = document.getElementsByTagName("article");
    for (let i = 0; i < articles.length; i++) {
      const categories = articles[i].getAttribute("category").split(", ");
      if (categories.includes(category)) {
        articles[i].style.display = "block";
      } else {
        articles[i].style.display = "none";
      }
    }
  }
  