import unittest
import json
from iga import create_app
from iga.models import Photo, Blog
from flask import url_for

class PhotoAPITest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        # Create some test photos
        photo1 = Photo(title='Photo 1', description='Description of photo 1', image='photo1.jpg')
        photo2 = Photo(title='Photo 2', description='Description of photo 2', image='photo2.jpg')
        photo3 = Photo(title='Photo 3', description='Description of photo 3', image='photo3.jpg')
        self.db.session.add_all([photo1, photo2, photo3])
        self.db.session.commit()

    def tearDown(self):
        Photo.query.delete()
        self.db.session.commit()

    def test_get_all_photos(self):
        response = self.client.get('/photos')
        self.assertEqual(response.status_code, 200)

        photos = json.loads(response.data)
        self.assertEqual(len(photos), 3)

        for photo in photos:
            self.assertIn('id', photo)
            self.assertIn('title', photo)
            self.assertIn('description', photo)
            self.assertIn('image', photo)
            self.assertEqual(photo['image'], url_for('static', filename=photo['image']))

    def test_get_photo_by_id(self):
        photo_id = Photo.query.first().id
        response = self.client.get('/photos/{}'.format(photo_id))
        self.assertEqual(response.status_code, 200)

        photo = json.loads(response.data)
        self.assertEqual(photo['id'], photo_id)
        self.assertEqual(photo['title'], Photo.query.get(photo_id).title)
        self.assertEqual(photo['description'], Photo.query.get(photo_id).description)
        self.assertEqual(photo['image'], url_for('static', filename=Photo.query.get(photo_id).image))

    def test_create_photo(self):
        data = {
            'title': 'New Photo',
            'description': 'Description of new photo',
            'image': 'new_photo.jpg'
        }

        response = self.client.post('/photos', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        new_photo = Photo.query.filter_by(title=data['title']).first()
        self.assertIsNotNone(new_photo)
        self.assertEqual(new_photo.title, data['title'])
        self.assertEqual(new_photo.description, data['description'])
        self.assertEqual(new_photo.image, data['image'])

    def test_update_photo(self):
        photo_id = Photo.query.first().id
        data = {
            'title': 'Updated Photo',
            'description': 'Updated description of photo',
            'image': 'updated_photo.jpg'
        }

        response = self.client.put('/photos/{}'.format(photo_id), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

        updated_photo = Photo.query.get(photo_id)
        self.assertEqual(updated_photo.title, data['title'])
        self.assertEqual(updated_photo.description, data['description'])
        self.assertEqual(updated_photo.image, data['image'])

    def test_delete_photo(self):
        photo_id = Photo.query.first().id
        response = self.client.delete('/photos/{}'.format(photo_id))
        self.assertEqual(response.status_code, 204)

        deleted_photo = Photo.query.get(photo_id)
        self.assertIsNone(deleted_photo)


class BlogAPITest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        # Create some test blogs
        blog1 = Blog(title='Blog Post 1', content='Content of blog post 1', author='John Doe')
        blog2 = Blog(title='Blog Post 2', content='Content of blog post 2', author='Jane Doe')
        blog3 = Blog(title='Blog Post 3', content='Content of blog post 3', author='Peter Jones')
        self.db.session.add_all([blog1, blog2, blog3])
        self.db.session.commit()

    def tearDown(self):
        Blog.query.delete()
        self.db.session.commit()

    def test_get_all_blogs(self):
        response = self.client.get('/blogs')
        self.assertEqual(response.status_code, 200)

        blogs = json.loads(response.data)
        self.assertEqual(len(blogs), 3)

        for blog in blogs:
            self.assertIn('id', blog)
            self.assertIn('title', blog)
            self.assertIn('content', blog)
            self.assertIn('author', blog)

    def test_get_blog_by_id(self):
        blog_id = Blog.query.first().id
        response = self.client.get('/blogs/{}'.format(blog_id))
        self.assertEqual(response.status_code, 200)

        blog = json.loads(response.data)
        self.assertEqual(blog['id'], blog_id)
        self.assertEqual(blog['title'], Blog.query.get(blog_id).title)
        self.assertEqual(blog['content'], Blog.query.get(blog_id).content)
        self.assertEqual(blog['author'], Blog.query.get(blog_id).author)

    def test_create_blog(self):
        data = {
            'title': 'New Blog Post',
            'content': 'Content of new blog post',
            'author': 'New Author'
        }

        response = self.client.post('/blogs', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        new_blog = Blog.query.filter_by(title=data['title']).first()
        self.assertIsNotNone(new_blog)
        self.assertEqual(new_blog.title, data['title'])
        self.assertEqual(new_blog.content, data['content'])
        self.assertEqual(new_blog.author, data['author'])

    def test_update_blog(self):
        blog_id = Blog.query.first().id
        data = {
            'title': 'Updated Blog Post',
            'content': 'Updated content of blog post',
            'author': 'Updated Author'
        }

        response = self.client.put('/blogs/{}'.format(blog_id), data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

        updated_blog = Blog.query.get(blog_id)
        self.assertEqual(updated_blog.title, data['title'])
        self.assertEqual(updated_blog.content, data['content'])
        self.assertEqual(updated_blog.author, data['author'])

    def test_delete_blog(self):
        blog_id = Blog.query.first().id
        response = self.client.delete('/blogs/{}'.format(blog_id))
        self.assertEqual(response.status_code, 204)

        deleted_blog = Blog.query.get(blog_id)
        self.assertIsNone(deleted_blog)


