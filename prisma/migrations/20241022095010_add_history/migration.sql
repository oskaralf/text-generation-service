/*
  Warnings:

  - You are about to drop the `dictionary` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the column `userId` on the `history` table. All the data in the column will be lost.
  - Added the required column `userName` to the `history` table without a default value. This is not possible if the table is not empty.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "dictionary";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "words" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "word" TEXT NOT NULL,
    "meaning" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "userName" TEXT NOT NULL,
    CONSTRAINT "words_userName_fkey" FOREIGN KEY ("userName") REFERENCES "User" ("name") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_history" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "level" REAL NOT NULL,
    "date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userName" TEXT NOT NULL,
    CONSTRAINT "history_userName_fkey" FOREIGN KEY ("userName") REFERENCES "User" ("name") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_history" ("date", "id", "level") SELECT "date", "id", "level" FROM "history";
DROP TABLE "history";
ALTER TABLE "new_history" RENAME TO "history";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
