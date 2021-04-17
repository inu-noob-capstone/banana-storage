package com.example.apptestbed

import java.io.*

class FileUtil {
    fun readTextFile(fullPath: String): String{
        // 이후 작성하는 코드는 이 안에 적는다.
        val file = File(fullPath)
        if(!file.exists()) return ""

        val reader = FileReader(file)
        val buffer = BufferedReader(reader)

        var temp =""
        val result = StringBuffer()

        while(true){
            temp = buffer.readLine()
            if (temp==null) break;
            else result.append(buffer)
        }

        buffer.close()
        return result.toString()
    }

    fun writeTextFile(directory: String, filename: String, content: String){
        // 이후 작성하는 코드는 이 안에 작성합니다.
        val dir = File(directory)
        if(!dir.exists()){
            dir.mkdirs()
        }

        val writer = FileWriter(directory + "/" + filename)
        val buffer = BufferedWriter(writer)

        buffer.write(content)
        buffer.close()
    }
}