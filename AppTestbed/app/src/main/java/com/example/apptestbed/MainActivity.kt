package com.example.apptestbed


import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.Message
import android.util.Log
import android.view.View
import com.example.apptestbed.databinding.ActivityMainBinding
import kotlinx.coroutines.*
import java.net.URL
import kotlin.concurrent.thread

suspend fun loadImage(imageUrl: String): Bitmap {
    val url = URL(imageUrl)
    val stream = url.openStream()
    return BitmapFactory.decodeStream(stream)
}

class MainActivity : AppCompatActivity() {

    val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        binding.buttonDownload.setOnClickListener {
            CoroutineScope(Dispatchers.Main).launch {
                binding.progress.visibility = View.VISIBLE

                val url = binding.editUrl.text.toString()
                val bitmap = withContext(Dispatchers.IO){
                    loadImage(url)
                }

                binding.imagePreview.setImageBitmap(bitmap)
                binding.progress.visibility = View.GONE
            }
        }

        var total = 0
        var started = false

        CoroutineScope(Dispatchers.Default).async {
            val deffered1 = async{
                delay(500)
                350
            }
            val deffered2 = async {
                delay(1000)
                200
            }
            Log.d("코루틴", "연산 결과 = ${deffered1.await() + deffered2.await()}")
        }

    }
}