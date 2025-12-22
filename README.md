# myAnimeTerminal

Welcome to **myAnimeTerminal**!

If you ever felt like anime recommendations don't quite hit the mark… well, you are in the right place.  
The sole purpose of this project is to use the **human component** as the main system to find related titles. Yes, it is quite simple, but there is more… To explain that to you,  
I need you to understand the beginning. Before there was anything, God created the heavens and the earth, but we do not have to go that far.

---

## How It Works

This system needs a reference title, which is just a fancy way to know what anime you like.  
Later, we use user data provided from **myAnimeList** (not stolen!) to find out what people (before you or I) found to be related to that reference.  

Often, recommendation systems leave what matters behind: the **human component**, quite capable of assuming relations if I do say so. For example, how did you  
feel when you watched *Akira* for the first time? That feeling of dystopian, mystery and modernism, which may fit Sci-fi genres, but it also can be attributed to other genres as well. And machines often fail to understand that.

---

## Origin

This idea came to me when I got injured and was stuck in bed, wanting to watch shows similar to Ghost in the Shell: Stand Alone Complex. Quite a naming there!  
But anyhow, the show itself isn’t as popular as I wanted, and recommendation systems didn’t give me good results, aside from Max Derrat’s suggestions.  

To make it clear: imagine eating a delicious meal, and a friend says, “Then, you should try this.”  
The plating may be different, but the taste will be similar. That’s the whole point of this project.

So I needed only to ask...

---

## Conventional Methods

**Long text here**... the content that could be ideal for you could be limited by the system itself. Netflix won't recommend Jin-Roh after you clicked Ghost in the Shell because it is not  
in its catalog. That system does work, but also, that fellow who believes that a particular show is so great that he has to tell everyone about it is represented in this app. And quite strong.

However, even the best systems struggle with **unknown related titles** because most metrics point to popular content. There are just too many things pointing in that direction.  
This project tries to circumvent that, though it sometimes fails too.

---

## Technical Details

- Each request returns a **JSON** containing more related titles, giving the system a console-style feel.  
- The app uses the **Jikan API**; about one request per second is safe.  
- Some animations limit the user from spamming - a feature or a bug? You decide.  
- The database is from 2014–2016. Future updates will use the same API while respecting Jikan’s rules.  
- The UI is built with **Tkinter**, simple but functional, even with some multitasking limitations.

---

## License & Usage

Finally, feel free to **use, modify, and adapt this code as you see fit**.  
You can even request permission from myAnimeList to use its database.  

Do what you want — this project is open for you to experiment with.
