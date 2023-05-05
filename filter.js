function filterProjects() {
    const category = document.getElementById("category").value;
    const articles = document.getElementsByTagName("article");
    for (let i = 0; i < articles.length; i++) {
      const article = articles[i];
      if (category === "all" || article.classList.contains(category)) {
        article.style.display = "";
      } else {
        article.style.display = "none";
      }
    }
  }
  
  document.getElementById("category").addEventListener("change", filterProjects);
  filterProjects();
  