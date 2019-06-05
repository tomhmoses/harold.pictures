import pickle

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

def main():
    albums = pickle.load( open( "albums.pk", "rb" ) )
    setPortfolioPage(albums)
    setAlbumPages(albums)

def setPortfolioPage(albums):
    f = open("templates/gallery-item-template.html", "rt")
    itemTemplate = f.read()
    f.close()
    f = open("templates/portfolio-template.html", "rt")
    portfolioTemplate = f.read()
    f.close()
    galleryItems = ""
    for album in albums:
        #print album.title
        galleryItem = itemTemplate
        galleryItem = galleryItem.replace("<!-- PRIMARYURL -->", album.coverPhoto.source)
        galleryItem = galleryItem.replace("<!-- ID -->", album.id)
        galleryItem = galleryItem.replace("<!-- TITLE -->", album.title)
        galleryItem = galleryItem.replace("<!-- DESCRIPTION -->", album.description)
        #print galleryItem
        galleryItems += "\n" + galleryItem
    portfolioTemplate = portfolioTemplate.replace("<!-- gallery-items-go-here-->", galleryItems)
    #print galleryItems
    f = open("portfolio.html", "w+")
    f.write(portfolioTemplate)
    f.close()

def setAlbumPages(albums):
    f = open("templates/single-gallery-item-template.html", "rt")
    itemTemplate = f.read()
    f.close()
    f = open("templates/portfolio-single-template.html", "rt")
    portfolioSingleTemplate = f.read()
    f.close()
    for count in range(len(albums)):
        portfolioSingle = portfolioSingleTemplate
        galleryItems = ""
        for photo in albums[count].photos:
            galleryItem = itemTemplate
            galleryItem = galleryItem.replace("<!-- SOURCE -->", photo.source)
            galleryItems += "\n" + galleryItem
        portfolioSingle = portfolioSingle.replace("<!-- single-gallery-items-go-here-->", galleryItems)
        print "-"*50
        print albums[count].title
        print "http://harold.tmos.es/album-" + albums[count].id + ".html"
        #print galleryItems
        portfolioSingle = portfolioSingle.replace("<!-- TITLE -->", albums[count].title)
        portfolioSingle = portfolioSingle.replace("<!-- DESCRIPTION -->", albums[count].description)
        portfolioSingle = portfolioSingle.replace("<!-- ID -->", albums[count].id)
        portfolioSingle = portfolioSingle.replace("<!-- PRIMARYURL -->", albums[count].coverPhoto.source)
        portfolioSingle = portfolioSingle.replace("<!-- PREV ALBUM LINK -->", "album-" + albums[count-1].id + ".html")
        portfolioSingle = portfolioSingle.replace("<!-- NEXT ALBUM LINK -->", "album-" + albums[(count+1)%len(albums)].id + ".html")
        portfolioSingle = portfolioSingle.replace("<!-- PREV ALBUM TITLE -->", albums[count-1].title)
        portfolioSingle = portfolioSingle.replace("<!-- NEXT ALBUM TITLE -->", albums[(count+1)%len(albums)].title)
        f = open("album-pages/album-" + albums[count].id + ".html", "w+")
        f.write(portfolioSingle)
        f.close()

if __name__ == '__main__':
    main()
