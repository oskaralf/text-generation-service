-- CreateTable
CREATE TABLE "history" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "level" REAL NOT NULL,
    "date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userId" TEXT NOT NULL,
    CONSTRAINT "history_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("name") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "dictionary" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "word" TEXT NOT NULL,
    "meaning" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "level" REAL NOT NULL,
    "userId" TEXT NOT NULL,
    CONSTRAINT "dictionary_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("name") ON DELETE RESTRICT ON UPDATE CASCADE
);
