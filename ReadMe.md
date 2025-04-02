### Article Manager Restful API

REST API endpoints guide for the article manager

## API Endpoints

### 1. Create Article
- **Method:** `POST`
- **URL:** `/articles`
- **Request Body:** JSON object containing:
  - `title` (string) – The title of the article. (Required)
  - `description` (string) – The description of the article. (Required)
  - `tags` (array) - An array of tags associated with the article, where each tag is a string.

- **Response:** 
  - **201 Created** – Returned if the article was successfully created, along with the details of the newly created article.

    **Example Response:**
    ```json
    {
      "title": "The Benefits of Omega-3 Fatty Acids 2",
      "description": "Omega-3 fatty acids are essential fats that offer numerous health benefits, including improving heart health, reducing inflammation, and enhancing brain function.",
      "tags": [
          "Health",
          "Nutrition",
          "Omega-3"
      ],
      "_id": "67ed88e69550173b298e993f"
    }
    ```

  - **400 Bad Request** – Returned if the `title` or `description` field is missing or empty.

    **Example Response:**
    ```json
    {
      "error": "The 'Title' and 'Description' fields are required!"
    }
    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while creating the article.

    **Example Response:**
    ```json
    {
      "error": "An unexpected error occured while creating the article"
    }
    ```

### 2. Insert Article Source & Trigger Celery Background Task
- **Method:** `PATCH`  
- **URL:** `/articles/<string:article_id>/sources`
- **Path Parameter:**
  - `article_id` (string) – The unique identifier of the article to which the source will be added.
- **Request Body:** JSON object containing:
  - `name` (string) – The name of the source.
  - `url` (string) – The URL of the source.
  - `text` (string) – A description or excerpt from the source.

- **Response:**
  - **201 Created** - Returned when the source is successfully added to the article, along with the details of the newly created source.

    **Example Response:**
    ```json
    {
      "article_id": "67ed88e69550173b298e993f",
      "name": "Health Benefits of Omega-3 Fatty Acids",
      "url": "https://www.medicalnewstoday.com/articles/324323",
      "text": "Omega-3 fatty acids play a vital role in brain function, inflammation, and cardiovascular health. This article highlights the evidence-based benefits of omega-3 and how they can improve overall health.",
      "parsed": false
    }
    ```

    > **Note:** The `parsed` field is automatically set to `false` upon source creation. After the source is created, a **Celery worker** will be triggered to update the `parsed` field from `false` to `true`.

  - **404 Not Found** - Returned if the given `article_id` is not found in the database.

    **Example Response:**
    ```json
    {
      "error": "Article id '67ed84889550173b298e993e' does not exist!"
    }
    ```

  - **400 Bad Request** - Returned if the `name`, `url`, or `text` field is missing or empty.

    **Example Response:**
    ```json
    {
      "error": "The 'Name', 'URL', and 'Text' source fields are required!"
    }
    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while adding the source.

    **Example Response:**
    ```json
    {
      "error": "An unexpected error occurred while adding the article source."
    }
    ```

### 3. Get Articles
- **Method:** `GET`  
- **URL:** `/articles`

- **Response:**
  - Returns all article documents in the database
  **Example Response:**
    ```json
    [
      {
        "_id": "67ed76e8291e70208e9d9a2f",
        "title": "Top 10 Superfoods for Immune Boosting",
        "description": "An exploration of nutrient-rich superfoods like garlic, spinach, and blueberries to boost your immune system.",
        "tags": ["Health", "Superfoods", "Immune System"],
        "sources": [
            {
                "name": "The Science of Yoga",
                "url": "https://www.psychologytoday.com/us/blog/urban-survival/201907/the-science-yoga-benefits-mental-health",
                "text": "Yoga has proven benefits for mental health, reducing symptoms of depression and anxiety.",
                "parsed": true
            }
        ]
      },
      {
        "_id": "67ed88e69550173b298e993f",
        "title": "The Benefits of Omega-3 Fatty Acids",
        "description": "Omega-3 fatty acids play a vital role in heart health, reducing inflammation, and improving brain function.",
        "tags": ["Health", "Nutrition", "Omega-3"]
      }
    ]

    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while fetching the articles.

    **Example Response:**
    ```json
    {
      "error": "An error occurred while fetching the data!"
    }
    ```

### 4. Get Article
- **Method:** `GET`  
- **URL:** `/articles/<string:article_id>`
- **Path Parameter:**
  - `article_id` (string) – The unique identifier of the article.

- **Response:**
  - Returns a specific article based on the `article_id`.

    **Example Response:**
    ```json
    {
      "_id": "67ed7aec291e70208e9d9a30",
      "title": "The Benefits of Yoga for Mental Health",
      "description": "Yoga is a powerful practice that can improve mental health, reduce stress, and increase emotional resilience. With various styles and techniques, yoga has become an essential tool for managing anxiety and depression.",
      "tags": [
        "Mental Health",
        "Yoga",
        "Stress Relief"
      ],
      "sources": [
        {
          "name": "Yoga and Mental Health: A Review of the Literature",
          "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3193651/",
          "text": "This review discusses the role of yoga in enhancing mental health, highlighting studies that show significant reductions in symptoms of PTSD, depression, and anxiety. The article also examines the physiological mechanisms by which yoga influences mental health, including the regulation of the autonomic nervous system.",
          "parsed": true
        }
      ]
    }
    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while fetching the article.

    **Example Response:**
    ```json
    {
      "error": "An error occurred while fetching the data!"
    }
    ```

### 5. Delete Article
- **Method:** `DELETE`  
- **URL:** `/articles/<string:article_id>`
- **Path Parameter:**
  - `article_id` (string) – The unique identifier of the article.

- **Response:**
  - **200 OK** - Returned when the article was successfully deleted.

    **Example Response:**
    ```json
    {
      "message": "Article Deleted"
    }
    ```

  - **404 Not Found** - Returned when the given `article_id` is not found in the database.

    **Example Response:**
    ```json
    {
      "error": "Invalid Article ID. No data deleted!"
    }
    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while deleting the article.

    **Example Response:**
    ```json
    {
      "error": "An unexpected error occurred!"
    }
    ```

### 6. Update Article
- **Method:** `PATCH`  
- **URL:** `/articles/<string:article_id>`
- **Path Parameter:**
  - `article_id` (string) – The unique identifier of the article to be updated.
- **Request Body:** JSON object containing:
  - `title` (string) – The title of the article. (Required)
  - `description` (string) – The description of the article. (Required)
  - `tags` (array) - An array of tags associated with the article, where each tag is a string.

- **Response:**
  - **200 OK** - Returned when the article was successfully updated.

    **Example Response:**
    ```json
    {
      "message": "Article updated successfully!"
    }
    ```

  - **400 Bad Request** - Returned if the `title` or `description` field is missing or empty.

    **Example Response:**
    ```json
    {
      "error": "The 'Title' and 'Description' fields are required!"
    }
    ```

  - **404 Not Found** - Returned when the `article_id` did not match any articles in the database.

    **Example Response:**
    ```json
    {
      "error": "Failed to update article. Article not found."
    }
    ```

  - **500 Internal Server Error** - Returned if an unexpected error occurs while updating the article.

    **Example Response:**
    ```json
    {
      "error": "An error occurred while updating the data!"
    }
    ```