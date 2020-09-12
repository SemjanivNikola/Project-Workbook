import * as firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/firestore'

// firebase init - add your own config here
const firebaseConfig = {
    apiKey: "AIzaSyBmfiTXgNyxlugNqVIrFshzEBtWfaeh3aU",
    authDomain: "zavrsni-cea71.firebaseapp.com",
    databaseURL: "https://zavrsni-cea71.firebaseio.com",
    projectId: "zavrsni-cea71",
    storageBucket: "zavrsni-cea71.appspot.com",
    messagingSenderId: "122434065323",
    appId: "1:122434065323:web:80a3f331c03694ea2c78ee"
}
firebase.initializeApp(firebaseConfig)

// utils
const db = firebase.firestore()
const auth = firebase.auth()

// collection references
const usersCollection = db.collection('users')
const postsCollection = db.collection('posts')
const commentsCollection = db.collection('comments')
const likesCollection = db.collection('likes')

// export utils/refs
export {
    db,
    auth,
    usersCollection,
    postsCollection,
    commentsCollection,
    likesCollection
}