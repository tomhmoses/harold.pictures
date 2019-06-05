import flickrapi
import pickle
import time

class HaroldAlbum:
    def __init__(self, id):
        self.id = id
        self.url = "https://www.flickr.com/photos/mosesharold/albums/" + id
        self.title = ""
        self.description = ""
        self.coverPhoto = None
        self.photos = []

    def __str__(self):
        string = "ID: " + self.id
        string += "\nURL: " + self.url
        string += "\nTITLE: " + self.title
        string += "\nDESC: " + self.description
        string += "\ncoverPhoto: " + str(self.coverPhoto)
        string += "\n PHOTOS:"
        for each in self.photos:
            string += "\n    " + str(each)
        return string



    def setDetails(self, title = "", description = "", coverPhoto = None, photos = []):
        self.title = title
        self.description = description
        self.coverPhoto = coverPhoto
        self.photos = photos

    def setPhotos(self, photos):
        self.photos = photos

def setAlbumDetails(flickr, album):
    print "nothing yet"

class HaroldPhoto:
    def __init__(self, id):
        self.id = id
        self.source = ""

    def __str__(self):
        return "ID: " + self.id + " SOURCE: " + self.source

    def setSource(self, source):
        self.source = source

def setPhotoSource(flickr, photo):
    photo.source = getOrigSource(flickr, photo.id)

def getOrigSource(flickr, photo_id):
    for eachSize in flickr.photos.getSizes(photo_id = photo_id)['sizes']['size']:
        if eachSize['label'] == 'Original':
            return eachSize['source']

def buildDataStructure(flickr,haroldID):
    albums = buildEmptyAlbums(flickr,haroldID)
    albums = fillAlbums(flickr,haroldID,albums)
    return albums

def buildEmptyAlbums(flickr,haroldID):
    photosets = flickr.photosets.getList(user_id=haroldID)['photosets']['photoset']
    albums = []
    for photoset in photosets:
        album = HaroldAlbum(photoset['id'])
        title = photoset['title']['_content']
        description = photoset['description']['_content']
        coverPhoto = HaroldPhoto(photoset['primary'])
        coverPhoto.setSource(getOrigSource(flickr, coverPhoto.id))
        album.setDetails(title, description, coverPhoto)
        albums.append(album)
        print "added album: " + album.title
    return albums

def fillAlbums(flickr,haroldID,albums):
    for album in albums:
        images = flickr.photosets.getPhotos(photoset_id=album.id, user_id=haroldID)['photoset']['photo']
        photos = []
        for image in images:
            # might need to deep copy list
            photo = HaroldPhoto(image['id'])
            photo.setSource(getOrigSource(flickr, photo.id))
            photos.append(photo)
        album.setPhotos(photos)
        print "filled album: " + album.title + " with " + str(len(album.photos)) + " photos"

        #sleeps 15 seconds to avoid spamming the api too much
        time.sleep(15)
    return albums

def main():
    #setup
    api_key = pickle.load( open( "api_key.pk", "rb" ) )
    api_secret = pickle.load( open( "api_secret.pk", "rb" ) )
    haroldID = '57729348@N02'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    #make and save albums
    albums = buildDataStructure(flickr, haroldID)
    pickle.dump(albums, open("albums.pk", "wb"))


if __name__ == '__main__':
    main()
