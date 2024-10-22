/*
  Warnings:

  - You are about to drop the column `meaning` on the `words` table. All the data in the column will be lost.
  - Added the required column `translation` to the `words` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_words" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "word" TEXT NOT NULL,
    "translation" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "userName" TEXT NOT NULL,
    CONSTRAINT "words_userName_fkey" FOREIGN KEY ("userName") REFERENCES "User" ("name") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_words" ("id", "language", "userName", "word") SELECT "id", "language", "userName", "word" FROM "words";
DROP TABLE "words";
ALTER TABLE "new_words" RENAME TO "words";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
