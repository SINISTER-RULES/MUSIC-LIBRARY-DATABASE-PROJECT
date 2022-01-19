from flask import Flask, render_template, url_for, request, flash, redirect
import mysql.connector
from base_connection import connect_database

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

connection = connect_database()

cursor = connection.cursor()

user = ''
user_name = ''
# team=''
team='& samiya'

####################### LOGIN PAGE #######################
@app.route('/')
def index_login():
    return render_template('index.html', team=team)

@app.route('/', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]

    global user
    user = username
    if username != 'admin':
        global user_name
        user_name = username

    cursor.execute("select * from users;")
    user_names = cursor.fetchall()
    for row in user_names:
        if row[0] != "admin" and row[0] == username and row[1] == password:
            return redirect(url_for('user_index'))
        if row[0] == "admin" and row[0] == username and row[1] == password:
            return redirect(url_for('admin_index'))
    return redirect(url_for('signup_values'))


####################### SIGNUP PAGE #######################
@app.route('/signup')
def signup():
    return render_template('signup.html', team=team)

@app.route('/signup', methods=['POST'])
def signup_values():
    username = request.form['username']
    password = request.form['password']

    global user
    user = username
    if username != 'admin':
        global user_name
        user_name = username
    # try:
        
    # except:
    #     return redirect(url_for('index_login'))
    com = "insert into users(username, password) values(%s, %s)"
    val = (username, password)
    cursor.execute(com, val)
    connection.commit()
    return redirect(url_for('user_index'))

####################### ADMIN USER CREATION PAGE #######################
@app.route('/user_creation')
def user_creation():
    global user
    user = "admin"
    cursor.execute("select * from user_creation;")
    music = cursor.fetchall()
    cursor.execute("select count(*) from user_creation")
    no_of_songs = cursor.fetchall()
    return render_template('user_creation.html', music=music, user=user, no_of_songs=no_of_songs, team=team)

####################### ADMIN SONGS PAGE #######################
@app.route('/admin_songs')
def admin_index():
    global user
    user = "admin"
    cursor.execute("select * from song")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    return render_template('admin_index.html', music=music, user=user, no_of_songs=no_of_songs, team=team)

####################### ADMIN SONG ADD PAGE #######################
@app.route('/admin_add')
def admin_add():
    global user
    user = "admin"
    return render_template('admin_add_song.html', user=user)

@app.route('/admin_add', methods=['POST'])
def admin_add_song():
    global user
    user = "admin"
    name = request.form['title']
    genre = request.form['genre']
    singer = request.form['singer']
    rating = request.form['rating']
    rel_year = request.form['rel_year']
    duration = request.form['duration']
    
    ## inserting into the table for songs
    com = " insert into song(name, genre, singer, rating, rel_year, duration) values(%s, %s, %s, %s, %s, %s);"
    val = (name, genre, singer, rating, rel_year, duration)
    cursor.execute(com, val)
    connection.commit()

    ## inserting into the table for singers
    com = " insert into singer(name, song_name, rating) values(%s, %s, %s);"
    val = (singer, name, rating)
    cursor.execute(com, val)
    connection.commit()

    ##inserting into table for 
    com = " insert into album(genre, song_name, singer_name) values(%s, %s, %s);"
    val = (genre, name, singer)
    cursor.execute(com, val)
    connection.commit()

    cursor.execute("select * from song where name='"+name+"';")
    music = cursor.fetchall()
    return render_template('admin_add_song.html', music=music, user=user)

####################### ADMIN SONG DELETE PAGE #######################
@app.route('/admin_delete')
def admin_delete():
    global user
    user = "admin"
    cursor.execute("select * from song;")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    return render_template('admin_delete_song.html',music=music, user=user, show='True',no_of_songs=no_of_songs)

@app.route('/admin_delete', methods=['POST'])
def admin_delete_song():
    global user
    user = "admin"
    name = request.form['title']
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    cursor.execute("select * from song where name='"+name+"';")
    music = cursor.fetchall()
    com = " delete from song where name='"+name+"';"
    cursor.execute(com)
    connection.commit()

    return render_template('admin_delete_song.html', music = music,  user=user, show='False',no_of_songs=no_of_songs), {"Refresh": "4; url=admin_delete"}


####################### ADMIN SONG EDIT PAGE #######################
@app.route('/admin_edit')
def admin_edit():
    global user
    user = "admin"
    cursor.execute("select * from song;")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    return render_template('admin_edit_song.html',music=music, user=user, show='True',no_of_songs=no_of_songs)

@app.route('/admin_edit', methods=['POST'])
def admin_edit_song():
    global user
    user = "admin"
    name = request.form['title']
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    cursor.execute("select * from song where name='"+name+"';")
    music = cursor.fetchall()
    return redirect(url_for('admin_editing', music=music, user=user))

@app.route('/admin_editing')
def admin_editing():
    global user
    user = "admin"
    m = request.args.get('music')
    cursor.execute("select * from song where name='"+m+"';")
    music = cursor.fetchall()
    return render_template('admin_editing.html', music=music, user=user)

@app.route('/admin_editing', methods=['POST'])
def admin_editing_form():
    global user
    user = "admin"
    m = request.args.get('music')
    cursor.execute("select * from song where name='"+m+"';")
    music = cursor.fetchall()

    name=request.form['title']
    genre = request.form['genre']
    singer = request.form['singer']
    rating = request.form['rating']
    rel_year = request.form['rel_year']
    duration = request.form['duration']

    # cursor.execute("delete from singer where name='"+music[0][2]+"';")
    # connection.commit()

    cursor.execute("delete from song where name='"+music[0][0]+"';")
    connection.commit()

    com = " insert into song(name, genre, singer, rating, rel_year, duration) values(%s, %s, %s, %s, %s, %s);"
    val = (name, genre, singer, rating, rel_year, duration)
    cursor.execute(com, val)
    connection.commit()

    com = "insert into singer(name, song_name, rating) values(%s, %s, %s);"
    val = (singer, name, rating)
    cursor.execute(com, val)
    connection.commit()

    cursor.execute("select * from song where name='"+name+"';")
    music = cursor.fetchall()

    return render_template('admin_editing.html', music=music, user=user), {"Refresh": "4; url=admin_edit"}

####################### ADMIN SINGERS PAGE #######################
@app.route('/singer')
def singer():
    global user
    user = "admin"
    cursor.execute("select singer, count(singer),round(avg(rating),2), round(avg(duration),2) from song group by singer;")
    singers = cursor.fetchall()
    cursor.execute("select count(distinct name) from singer;")
    no_of_singers = cursor.fetchall()
    return render_template('singer.html', singers = singers, user=user, no_of_singers=no_of_singers)

@app.route('/singer_songs')
def singer_songs():
    global user
    user = "admin"
    name = request.args.get('name')
    cursor.execute("select * from song where singer='"+name+"';")
    songs = cursor.fetchall()
    
    cursor.execute("select count(*) from song where singer='"+name+"';")
    no_of_songs = cursor.fetchall()
    return render_template('singer_songs.html', name=name, music=songs, user=user, no_of_songs=no_of_songs)

####################### ADMIN DELETE SINGERS PAGE #######################
@app.route('/singer_delete')
def singer_delete():
    global user
    user = "admin"
    cursor.execute("select singer, count(singer),round(avg(rating),2), round(avg(duration),2) from song group by singer;")
    singers = cursor.fetchall()
    cursor.execute("select count(distinct name) from singer;")
    no_of_singers = cursor.fetchall()
    return render_template('singer_delete.html', singer = singers, user=user, show='True', no_of_singers=no_of_singers)

@app.route('/singer_delete', methods=['POST'])
def singer_songs_delete():
    name = request.form['name']
    
    cursor.execute("select singer, count(singer),round(avg(rating),2), round(avg(duration),2) from song where singer='"+name+"' group by singer;")
    singers = cursor.fetchall()

    cursor.execute("select * from song where singer='"+name+"';")
    music = cursor.fetchall()
    
    cursor.execute("delete from song where singer='"+name+"';")
    connection.commit()

    return render_template('singer_delete.html', singer = singers,music=music,  user=user, show='False'), {"Refresh": "4; url=singer_delete"}

    return redirect(url_for('singer'))




##############################################################################################
######################################### USER ###############################################
##############################################################################################


####################### USER SONGS PAGE #######################    
@app.route('/user_songs')
def user_index():
    global user
    user = user_name
    cursor.execute("select * from song")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song")
    no_of_songs = cursor.fetchall()
    return render_template('user_index.html', music=music, user=user, no_of_songs=no_of_songs, team=team)

####################### USER SINGERS PAGE #######################
@app.route('/user_singer')
def user_singer():
    global user
    user = user_name
    cursor.execute("select singer, count(singer),round(avg(rating),2), round(avg(duration),2) from song group by singer;")
    singers = cursor.fetchall()
    cursor.execute("select count(distinct name) from singer;")
    no_of_singers = cursor.fetchall()
    return render_template('user_singer.html', singers = singers, user=user, no_of_singers=no_of_singers, page='singer')

@app.route('/user_singer_songs')
def user_singer_songs():
    global user
    user = user_name
    name = request.args.get('name')
    cursor.execute("select * from song where singer='"+name+"';")
    songs = cursor.fetchall()
    cursor.execute("select count(*) from song where singer='"+name+"';")
    no_of_songs = cursor.fetchall()
    return render_template('user_singer_songs.html', name=name, music=songs, user=user, page='singer',no_of_songs=no_of_songs)
    

####################### USER ALBUMS PAGE #######################
@app.route('/user_albums')
def user_albums():
    global user
    user = user_name
    cursor.execute("select genre, count(genre),round(avg(rating),2), round(avg(duration),2) from song group by genre;")
    singers = cursor.fetchall()
    cursor.execute("select count(distinct genre) from song;")
    no_of_singers = cursor.fetchall()
    return render_template('user_album.html', singers = singers, user=user, no_of_singers=no_of_singers, page='albums')

@app.route('/user_albums_songs')
def user_albums_songs():
    global user
    user = user_name
    name = request.args.get('name')
    cursor.execute("select * from song where genre='"+name+"';")
    songs = cursor.fetchall()
    cursor.execute("select count(*) from song where genre='"+name+"';")
    no_of_songs = cursor.fetchall()
    return render_template('user_album_songs.html', name=name, music=songs, user=user, page='albums', no_of_songs=no_of_songs)

####################### USER PLAYLIST PAGE #######################    
@app.route('/user_playlist', methods=['GET'])
def user_playlist():
    global user
    cursor.execute("select name, count(name), round(avg(rating),2), round(avg(duration),2) from playlist group by name;")
    music = cursor.fetchall()

    cursor.execute("select count(distinct name) from playlist;")
    no_of_playlist = cursor.fetchall()

    cursor.execute("select count(name), round(avg(rating),2), round(avg(duration),2) from playlist group by name;")
    no_of_songs = cursor.fetchall()
    return render_template('user_playlist.html', music=music, user=user, no_of_songs=no_of_songs, no_of_playlist=no_of_playlist)

@app.route('/user_playlist_songs')
def user_playlist_songs():
    global user
    user = user_name
    name = request.args.get('name')
    cursor.execute('select s.* from song s, playlist p where p.name="'+name+'" and p.song_name=s.name;')
    songs = cursor.fetchall()
    cursor.execute('select count(*) from playlist where name="'+name+'";')
    no_of_songs = cursor.fetchall()
    return render_template('user_playlist_songs.html', name=name, music=songs, user=user, page='singer',no_of_songs=no_of_songs)


####################### USER PLAYLIST ADD PAGE #######################    
@app.route('/user_playlist_add', methods=['POST', 'GET'])
def user_playlist_add():
    global user
    user = user_name


    if request.method == 'POST':
        title = request.form['title']
        print(title)
        print(request.form.getlist('song_name'))
        songs = request.form.getlist('song_name')
        for songs in songs:
            com = 'insert into playlist (name, song_name, rating, duration) values(%s, %s, %s, %s);'
            cursor.execute('select rating, duration from song where name="'+songs+'";')
            rating_duration = cursor.fetchall()
            values = (title, songs, rating_duration[0][0], rating_duration[0][1])
            cursor.execute(com,values)
            connection.commit()
        return redirect(url_for('user_playlist'))

    cursor.execute("select * from song;")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song;")
    no_of_songs = cursor.fetchall()
    return render_template('user_playlist_add.html', music=music, user=user, no_of_songs=no_of_songs)



####################### USER DELETE PLAYLIST PAGE #######################
@app.route('/playlist_delete')
def user_playlist_delete():
    global user
    user = user_name
    cursor.execute("select name, count(name),round(avg(rating),2), round(avg(duration),2) from playlist group by name;")
    singers = cursor.fetchall()
    cursor.execute("select count(distinct name) from playlist;")
    no_of_singers = cursor.fetchall()
    return render_template('user_playlist_delete.html', singer = singers, user=user, show='True', no_of_singers=no_of_singers)

@app.route('/playlist_delete', methods=['POST'])
def playlist_songs_delete():
    name = request.form['name']
    
    cursor.execute('select name, count(name), round(avg(rating),2), round(avg(duration),2) from playlist where name="'+name+'";')
    singers = cursor.fetchall()

    cursor.execute('select s.* from song s, playlist p where p.name="'+name+'" and p.song_name=s.name;')
    music = cursor.fetchall()
    
    cursor.execute('delete from playlist where name="'+name+'";')
    connection.commit()

    return render_template('user_playlist_delete.html', singer = singers,music=music,  user=user, show='False'), {"Refresh": "4; url=playlist_delete"}

    return redirect(url_for('playlist_delete'))



####################### USER PLAYLIST EDIT PAGE #######################
@app.route('/user_edit')
def user_edit():
    global user
    user = user_name
    cursor.execute('select name, count(name), round(avg(rating),2), round(avg(duration),2) from playlist group by name;')
    music = cursor.fetchall()
    return render_template('user_playlist_edit.html',music=music, user=user, show='True')

@app.route('/user_edit', methods=['POST'])
def user_edit_playlist():
    global user
    user = user_name
    name = request.form['title']
    
    return redirect(url_for('user_editing', music=name, user=user))

@app.route('/user_editing')
def user_editing():
    global user
    user = user_name
    m = request.args.get('name')

    
    cursor.execute("select * from song s;")
    music = cursor.fetchall()

    cursor.execute('select s.name from song s, playlist p where p.name="'+str(m)+'" and p.song_name=s.name;')
    music_in_my_playlist = cursor.fetchall()

    cursor.execute('select count(*) from playlist where name="'+str(m)+'";')
    no_of_songs = cursor.fetchall()


    return render_template('user_playlist_editing.html', music=music, user=user,no_of_songs=no_of_songs, playlist_name=m, music_in_my_playlist=music_in_my_playlist)

@app.route('/user_editing', methods=['POST', 'GET'])
def user_editing_playlist():
    global user
    user = user_name


    if request.method == 'POST':
        m = request.args.get('name')
        cursor.execute('delete from playlist where name="'+str(m)+'";')
        connection.commit()
        title = request.form['title']
        print(title)
        print(request.form.getlist('song_name'))
        songs = request.form.getlist('song_name')
        for songs in songs:
            com = "insert into playlist (name, song_name, rating, duration) values(%s, %s, %s, %s);"
            cursor.execute('select rating, duration from song where name="'+songs+'";')
            rating_duration = cursor.fetchall()
            values = (title, songs, rating_duration[0][0], rating_duration[0][1])
            cursor.execute(com,values)
            connection.commit()
        return redirect(url_for('user_playlist'))

    cursor.execute("select * from song;")
    music = cursor.fetchall()
    cursor.execute("select count(*) from song;")
    no_of_songs = cursor.fetchall()
    return redirect(url_for('user_playlist_add.html', music=music, user=user, no_of_songs=no_of_songs))


if __name__ == '__main__':
    app.run(debug=True)
