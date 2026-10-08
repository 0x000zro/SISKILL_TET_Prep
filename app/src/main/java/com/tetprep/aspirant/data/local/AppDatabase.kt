package com.tetprep.aspirant.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.tetprep.aspirant.data.local.dao.BookmarkDao
import com.tetprep.aspirant.data.local.dao.MicroTopicDao
import com.tetprep.aspirant.data.local.dao.MockTestDao
import com.tetprep.aspirant.data.local.dao.QuestionDao
import com.tetprep.aspirant.data.local.dao.SubjectDao
import com.tetprep.aspirant.data.local.dao.SubtopicDao
import com.tetprep.aspirant.data.local.dao.TopicDao
import com.tetprep.aspirant.data.local.dao.UserProgressDao
import com.tetprep.aspirant.data.local.entity.BookmarkEntity
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.MockTestEntity
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.data.local.entity.SubjectEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.data.local.entity.UserProgressEntity
import com.tetprep.aspirant.utils.Constants

@Database(
    entities = [
        SubjectEntity::class,
        TopicEntity::class,
        SubtopicEntity::class,
        MicroTopicEntity::class,
        QuestionEntity::class,
        UserProgressEntity::class,
        BookmarkEntity::class,
        MockTestEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun subjectDao(): SubjectDao
    abstract fun topicDao(): TopicDao
    abstract fun subtopicDao(): SubtopicDao
    abstract fun microTopicDao(): MicroTopicDao
    abstract fun questionDao(): QuestionDao
    abstract fun userProgressDao(): UserProgressDao
    abstract fun bookmarkDao(): BookmarkDao
    abstract fun mockTestDao(): MockTestDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    Constants.DATABASE_NAME
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
