# Udemy Django Course
2020, TravelPerk.

## Current API endpoints

/api/recipe/	rest_framework.routers.APIRootView	recipe:api-root
/api/recipe/\.<format>/	rest_framework.routers.APIRootView	recipe:api-root
/api/recipe/ingredients/	recipe.views.IngredientViewSet	recipe:ingredient-list
/api/recipe/ingredients\.<format>/	recipe.views.IngredientViewSet	recipe:ingredient-list
/api/recipe/recipes/	recipe.views.RecipeViewSet	recipe:recipe-list
/api/recipe/recipes/<pk>/	recipe.views.RecipeViewSet	recipe:recipe-detail
/api/recipe/recipes/<pk>/upload-image/	recipe.views.RecipeViewSet	recipe:recipe-upload-image
/api/recipe/recipes/<pk>/upload-image\.<format>/	recipe.views.RecipeViewSet	recipe:recipe-upload-image
/api/recipe/recipes/<pk>\.<format>/	recipe.views.RecipeViewSet	recipe:recipe-detail
/api/recipe/recipes\.<format>/	recipe.views.RecipeViewSet	recipe:recipe-list
/api/recipe/tags/	recipe.views.TagViewSet	recipe:tag-list
/api/recipe/tags\.<format>/	recipe.views.TagViewSet	recipe:tag-list
/api/user/create/	user.views.CreateUserView	user:create
/api/user/profile/	user.views.ManageUserView	user:logged_user
/api/user/token/	user.views.CreateTokenView	user:token
/media/<path>	django.views.static.serve

## Useful docker commands

'''
docker-compose build
docker-compose run
docker-compose run app sh -c 'python manage.py test && flake8'
docker-compose run app sh -c 'python manage.py show_urls'
'''
