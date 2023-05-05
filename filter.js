function filterByCategory(category) {
    const articles = document.querySelectorAll('article');
    articles.forEach((article) => {
      const categoryElement = article.querySelector('h3');
      if (categoryElement.innerText !== category) {
        article.style.display = 'none';
      } else {
        article.style.display = 'block';
      }
    });
  }
  